"""
Evaluator Agent - Wrapper for evaluation functionality
"""

from ..evaluation.evaluator import Evaluator as EvaluationEngine


class EvaluatorAgent:
    """
    Evaluator Agent provides quality assessment for all outputs
    """
    
    def __init__(self):
        """Initialize Evaluator Agent"""
        self.evaluator = EvaluationEngine()
    
    def evaluate_summary(self, summary: str, reference: str, summary_type: str = "executive") -> Dict:
        """Evaluate summary quality"""
        return self.evaluator.evaluate_summary(summary, reference, summary_type)
    
    def evaluate_extractions(self, extractions: Dict, document: Dict) -> Dict:
        """Evaluate extraction quality"""
        return self.evaluator.evaluate_extractions(extractions, document)
    
    def evaluate_qa(self, qa_result: Dict, document: Dict) -> Dict:
        """Evaluate Q&A quality"""
        return self.evaluator.evaluate_qa(qa_result, document)

