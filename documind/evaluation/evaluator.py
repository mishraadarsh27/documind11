"""
Evaluator Agent - Assesses output quality and provides improvement suggestions
"""

from typing import Dict, Optional
from loguru import logger

from .metrics import EvaluationMetrics


class Evaluator:
    """
    Evaluator Agent assesses the quality of generated outputs:
    - Summary quality (clarity, correctness, completeness)
    - Citation accuracy
    - Extraction precision and recall
    """
    
    def __init__(self):
        """Initialize Evaluator"""
        self.metrics = EvaluationMetrics()
    
    def evaluate_summary(self, summary: str, reference: str, summary_type: str = "executive") -> Dict:
        """
        Evaluate summary quality
        
        Args:
            summary: Generated summary
            reference: Reference/original text
            summary_type: Type of summary (executive, bullet, tldr)
        
        Returns:
            Evaluation results dictionary
        """
        evaluation = {
            "summary_type": summary_type,
            "rouge_scores": {},
            "clarity": 0.0,
            "completeness": 0.0,
            "overall_score": 0.0,
            "suggestions": []
        }
        
        # Calculate ROUGE scores
        try:
            evaluation["rouge_scores"] = self.metrics.calculate_rouge(summary, reference)
        except Exception as e:
            logger.error(f"Error calculating ROUGE: {e}")
        
        # Calculate clarity
        evaluation["clarity"] = self.metrics.calculate_clarity(summary)
        
        # Calculate completeness
        evaluation["completeness"] = self.metrics.calculate_completeness(summary, reference)
        
        # Calculate overall score (weighted average)
        rouge_f = evaluation["rouge_scores"].get("rougeL", {}).get("fmeasure", 0.0) if evaluation["rouge_scores"] else 0.0
        evaluation["overall_score"] = (
            rouge_f * 0.4 +
            evaluation["clarity"] * 0.3 +
            evaluation["completeness"] * 0.3
        )
        
        # Generate suggestions
        evaluation["suggestions"] = self._generate_suggestions(evaluation)
        
        return evaluation
    
    def evaluate_extractions(self, extractions: Dict, document: Dict) -> Dict:
        """
        Evaluate extraction quality
        
        Args:
            extractions: Extracted data dictionary
            document: Original document
        
        Returns:
            Evaluation results
        """
        evaluation = {
            "tables": {"count": 0, "quality": 0.0},
            "metrics": {"count": 0, "quality": 0.0},
            "dates": {"count": 0, "quality": 0.0},
            "tasks": {"count": 0, "quality": 0.0},
            "entities": {"count": 0, "quality": 0.0},
            "overall_score": 0.0
        }
        
        # Evaluate each extraction type
        for ext_type in ["tables", "metrics", "dates", "tasks", "entities"]:
            ext_data = extractions.get(ext_type, [])
            if isinstance(ext_data, dict):
                ext_data = ext_data.get("all", [])
            
            evaluation[ext_type]["count"] = len(ext_data) if isinstance(ext_data, list) else 0
            
            # Simple quality heuristic (can be improved)
            if ext_data:
                evaluation[ext_type]["quality"] = min(1.0, len(ext_data) / 10.0)  # Normalize
        
        # Calculate overall score
        scores = [evaluation[ext_type]["quality"] for ext_type in evaluation if ext_type != "overall_score"]
        evaluation["overall_score"] = sum(scores) / len(scores) if scores else 0.0
        
        return evaluation
    
    def evaluate_qa(self, qa_result: Dict, document: Dict) -> Dict:
        """
        Evaluate Q&A quality
        
        Args:
            qa_result: Q&A result dictionary
            document: Original document
        
        Returns:
            Evaluation results
        """
        evaluation = {
            "answer_quality": 0.0,
            "citation_accuracy": 0.0,
            "confidence": qa_result.get("confidence", 0.0),
            "overall_score": 0.0,
            "suggestions": []
        }
        
        # Evaluate citation accuracy
        citations = qa_result.get("citations", [])
        evaluation["citation_accuracy"] = self.metrics.calculate_citation_accuracy(citations, document)
        
        # Answer quality based on length and confidence
        answer = qa_result.get("answer", "")
        answer_length_score = min(1.0, len(answer.split()) / 50.0)  # Optimal around 50 words
        evaluation["answer_quality"] = (
            answer_length_score * 0.5 +
            evaluation["confidence"] * 0.5
        )
        
        # Overall score
        evaluation["overall_score"] = (
            evaluation["answer_quality"] * 0.4 +
            evaluation["citation_accuracy"] * 0.4 +
            evaluation["confidence"] * 0.2
        )
        
        # Generate suggestions
        if evaluation["citation_accuracy"] < 0.7:
            evaluation["suggestions"].append("Improve citation accuracy by verifying page references")
        if evaluation["confidence"] < 0.6:
            evaluation["suggestions"].append("Answer confidence is low. Consider refining the question or document context.")
        
        return evaluation
    
    def _generate_suggestions(self, evaluation: Dict) -> list:
        """Generate improvement suggestions based on evaluation"""
        suggestions = []
        
        if evaluation["clarity"] < 0.6:
            suggestions.append("Improve clarity by using shorter sentences and simpler language")
        
        if evaluation["completeness"] < 0.6:
            suggestions.append("Increase completeness by including more key points from the original document")
        
        rouge_f = evaluation["rouge_scores"].get("rougeL", {}).get("fmeasure", 0.0) if evaluation["rouge_scores"] else 0.0
        if rouge_f < 0.5:
            suggestions.append("Improve summary quality by better capturing the essence of the original text")
        
        if evaluation["overall_score"] < 0.6:
            suggestions.append("Overall quality can be improved. Review all aspects of the summary.")
        
        return suggestions

