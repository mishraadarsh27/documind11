"""
DocuMind Orchestrator - Main coordinator for all agents
"""

import os
from typing import Dict, List, Optional, Any
from pathlib import Path
import hashlib
from loguru import logger
from datetime import datetime

from .agents.reader import ReaderAgent
from .agents.extractor import ExtractorAgent
from .agents.analyzer import AnalyzerAgent
from .agents.qa_agent import QAAgent
from .agents.memory import MemoryAgent
from .agents.evaluator import EvaluatorAgent


class DocuMind:
    """
    Main DocuMind orchestrator that coordinates all agents
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        ocr_enabled: bool = True,
        memory_enabled: bool = True,
        evaluation_enabled: bool = True,
        storage_path: str = "./memory_bank",
        use_free_models: bool = True
    ):
        """
        Initialize DocuMind
        
        Args:
            api_key: OpenAI API key (optional if use_free_models=True)
            ocr_enabled: Enable OCR functionality
            memory_enabled: Enable memory system
            evaluation_enabled: Enable evaluation
            storage_path: Path for memory storage
            use_free_models: Use FREE Hugging Face models instead of OpenAI (default: True)
        """
        self.use_free_models = use_free_models
        
        # Initialize agents
        self.reader = ReaderAgent(ocr_enabled=ocr_enabled)
        self.extractor = ExtractorAgent()
        
        # Use FREE models by default
        if use_free_models:
            logger.info("Using FREE Hugging Face models - No API key required!")
            self.analyzer = AnalyzerAgent()  # FREE - no API key needed
            self.qa = QAAgent()  # FREE - no API key needed
        else:
            # Use OpenAI (requires API key)
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                logger.warning("OpenAI API key not provided. Switching to FREE models.")
                self.analyzer = AnalyzerAgent()
                self.qa = QAAgent()
                self.use_free_models = True
            else:
                # Use OpenAI (would need separate OpenAI agent files)
                logger.warning("OpenAI mode not fully implemented. Using FREE models instead.")
                self.analyzer = AnalyzerAgent()
                self.qa = QAAgent()
                self.use_free_models = True
        
        self.memory = MemoryAgent(storage_path=storage_path) if memory_enabled else None
        self.evaluator = EvaluatorAgent() if evaluation_enabled else None
        
        # Current document state
        self.current_document = None
        self.current_document_id = None
        
        logger.info("DocuMind initialized")
    
    def process_document(
        self,
        source: str,
        tasks: Optional[List[str]] = None,
        document_id: Optional[str] = None,
        store_in_memory: bool = True
    ) -> Dict:
        """
        Process a document with specified tasks
        
        Args:
            source: Path to document or URL
            tasks: List of tasks to perform (extract, summarize, qa, evaluate)
                   If None, performs all tasks
            document_id: Optional document identifier
            store_in_memory: Whether to store results in memory
        
        Returns:
            Dictionary with all results
        """
        if tasks is None:
            tasks = ["extract", "summarize"]
        
        logger.info(f"Processing document: {source} with tasks: {tasks}")
        
        # Generate document ID if not provided
        if not document_id:
            document_id = self._generate_document_id(source)
        
        # Step 1: Read document
        document = self.reader.read_document(source)
        self.current_document = document
        self.current_document_id = document_id
        
        # Add to session memory
        if self.memory:
            self.memory.add_document_to_session(document_id, document)
        
        results = {
            "document_id": document_id,
            "document": document,
            "extractions": {},
            "summaries": {},
            "qa": None,
            "evaluations": {},
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "tasks": tasks,
                "source": source
            }
        }
        
        # Step 2: Extract information
        if "extract" in tasks:
            logger.info("Extracting information...")
            extractions = self.extractor.extract_all(document)
            results["extractions"] = extractions
            
            if self.memory:
                self.memory.store_insights(document_id, extractions, document.get("metadata"), persist=store_in_memory)
        
        # Step 3: Generate summaries
        if "summarize" in tasks:
            if self.analyzer:
                logger.info("Generating summaries using FREE models...")
                summaries = self.analyzer.generate_summaries(document)
                results["summaries"] = summaries
                
                if self.memory:
                    self.memory.store_summaries(document_id, summaries)
            else:
                logger.warning("Analyzer not available. Skipping summarization.")
                results["summaries"] = {}
        
        # Step 4: Set up Q&A
        if "qa" in tasks:
            if self.qa:
                logger.info("Setting up Q&A system with FREE models...")
                self.qa.setup_document(document)
                results["qa"] = self.qa
            else:
                logger.warning("Q&A agent not available. Skipping Q&A setup.")
        
        # Step 5: Evaluate outputs
        if "evaluate" in tasks and self.evaluator:
            logger.info("Evaluating outputs...")
            evaluations = {}
            
            if results.get("summaries"):
                for summary_type, summary_text in results["summaries"].items():
                    evaluations[f"summary_{summary_type}"] = self.evaluator.evaluate_summary(
                        summary_text,
                        document.get("text", ""),
                        summary_type
                    )
            
            if results.get("extractions"):
                evaluations["extractions"] = self.evaluator.evaluate_extractions(
                    results["extractions"],
                    document
                )
            
            results["evaluations"] = evaluations
        
        logger.info(f"Document processing complete: {document_id}")
        return results
    
    def answer_question(self, question: str, return_citations: bool = True) -> Dict:
        """
        Answer a question about the current document
        
        Args:
            question: User question
            return_citations: Whether to include citations
        
        Returns:
            Answer dictionary
        """
        if not self.qa:
            return {
                "answer": "Q&A system not available. Please process document with Q&A enabled first.",
                "citations": [],
                "confidence": 0.0
            }
        
        if not self.current_document:
            return {
                "answer": "No document loaded. Please process a document first.",
                "citations": [],
                "confidence": 0.0
            }
        
        answer = self.qa.answer(question, return_citations=return_citations)
        
        # Store in memory
        if self.memory:
            self.memory.add_qa_to_history(question, answer)
        
        # Evaluate if evaluator is available
        if self.evaluator:
            evaluation = self.evaluator.evaluate_qa(answer, self.current_document)
            answer["evaluation"] = evaluation
        
        return answer
    
    def get_summary(self, summary_type: str = "executive") -> Optional[str]:
        """
        Get a specific summary type
        
        Args:
            summary_type: Type of summary (executive, bullet, tldr)
        
        Returns:
            Summary text or None
        """
        if not self.current_document_id or not self.memory:
            return None
        
        summaries = self.memory.session_memory.context.get("summaries", {}).get(self.current_document_id, {})
        return summaries.get(summary_type)
    
    def get_extractions(self) -> Optional[Dict]:
        """Get extracted information"""
        if not self.current_document_id or not self.memory:
            return None
        
        return self.memory.session_memory.context.get("extractions", {}).get(self.current_document_id)
    
    def search_memory(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search across stored insights
        
        Args:
            query: Search query
            limit: Maximum results
        
        Returns:
            List of matching insights
        """
        if not self.memory:
            return []
        
        return self.memory.search_insights(query, limit)
    
    def _generate_document_id(self, source: str) -> str:
        """Generate unique document ID from source"""
        source_hash = hashlib.md5(source.encode()).hexdigest()
        return f"doc_{source_hash[:12]}"
    
    def resume_from_checkpoint(self, checkpoint_id: str) -> Dict:
        """
        Resume processing from a checkpoint
        
        Args:
            checkpoint_id: Checkpoint identifier
        
        Returns:
            Document results
        """
        # This is a placeholder for checkpoint functionality
        # In a full implementation, this would load saved state
        logger.info(f"Resuming from checkpoint: {checkpoint_id}")
        # Implementation would load checkpoint data and continue processing
        return {}

