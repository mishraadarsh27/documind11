"""
Memory Agent - Manages both session and long-term memory
"""

from typing import Dict, Optional
from loguru import logger

from ..memory.memory_bank import MemoryBank
from ..memory.session_memory import SessionMemory


class MemoryAgent:
    """
    Memory Agent coordinates session-level and long-term memory
    """
    
    def __init__(self, storage_path: str = "./memory_bank", session_id: Optional[str] = None):
        """
        Initialize Memory Agent
        
        Args:
            storage_path: Path for long-term memory storage
            session_id: Optional session identifier
        """
        self.memory_bank = MemoryBank(storage_path)
        self.session_memory = SessionMemory(session_id)
        logger.info(f"Memory Agent initialized with session: {self.session_memory.session_id}")
    
    def store_insights(self, document_id: str, insights: Dict, metadata: Optional[Dict] = None, persist: bool = True):
        """
        Store insights in both session and long-term memory
        
        Args:
            document_id: Document identifier
            insights: Insights to store
            metadata: Optional metadata
            persist: Whether to persist to long-term memory
        """
        # Store in session memory
        self.session_memory.store_extractions(document_id, insights)
        
        # Store in long-term memory if requested
        if persist:
            self.memory_bank.store_insights(document_id, insights, metadata)
        
        logger.info(f"Stored insights for document: {document_id}")
    
    def retrieve_insights(self, document_id: str, from_long_term: bool = True) -> Optional[Dict]:
        """
        Retrieve insights from memory
        
        Args:
            document_id: Document identifier
            from_long_term: Whether to check long-term memory
        
        Returns:
            Stored insights or None
        """
        # Check session memory first
        session_extractions = self.session_memory.context.get("extractions", {}).get(document_id)
        if session_extractions:
            return session_extractions
        
        # Check long-term memory
        if from_long_term:
            long_term_data = self.memory_bank.retrieve_insights(document_id)
            if long_term_data:
                return long_term_data.get("insights")
        
        return None
    
    def search_insights(self, query: str, limit: int = 10) -> list:
        """Search across all stored insights"""
        return self.memory_bank.search_insights(query, limit)
    
    def get_session_context(self) -> Dict:
        """Get current session context"""
        return self.session_memory.get_context()
    
    def add_document_to_session(self, document_id: str, document: Dict):
        """Add document to current session"""
        self.session_memory.add_document(document_id, document)
    
    def store_summaries(self, document_id: str, summaries: Dict):
        """Store summaries in session memory"""
        self.session_memory.store_summaries(document_id, summaries)
    
    def add_qa_to_history(self, question: str, answer: Dict):
        """Add Q&A to session history"""
        self.session_memory.add_qa_pair(question, answer)
    
    def compact_memory(self, max_age_days: int = 90):
        """Compact long-term memory"""
        self.memory_bank.compact_memory(max_age_days)

