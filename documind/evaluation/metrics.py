"""
Evaluation Metrics - ROUGE, clarity, completeness scoring
"""

from typing import Dict, List, Optional
from rouge_score import rouge_scorer
from loguru import logger
import nltk

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass


class EvaluationMetrics:
    """Calculate evaluation metrics for summaries and extractions"""
    
    def __init__(self):
        """Initialize evaluation metrics"""
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    def calculate_rouge(self, summary: str, reference: str) -> Dict:
        """
        Calculate ROUGE scores
        
        Args:
            summary: Generated summary
            reference: Reference text
        
        Returns:
            Dictionary with ROUGE scores
        """
        try:
            scores = self.rouge_scorer.score(reference, summary)
            return {
                "rouge1": {
                    "precision": scores['rouge1'].precision,
                    "recall": scores['rouge1'].recall,
                    "fmeasure": scores['rouge1'].fmeasure
                },
                "rouge2": {
                    "precision": scores['rouge2'].precision,
                    "recall": scores['rouge2'].recall,
                    "fmeasure": scores['rouge2'].fmeasure
                },
                "rougeL": {
                    "precision": scores['rougeL'].precision,
                    "recall": scores['rougeL'].recall,
                    "fmeasure": scores['rougeL'].fmeasure
                }
            }
        except Exception as e:
            logger.error(f"Error calculating ROUGE: {e}")
            return {}
    
    def calculate_clarity(self, text: str) -> float:
        """
        Calculate clarity score (0-1)
        Based on sentence length, word complexity, etc.
        
        Args:
            text: Text to evaluate
        
        Returns:
            Clarity score
        """
        if not text:
            return 0.0
        
        sentences = nltk.sent_tokenize(text)
        if not sentences:
            return 0.0
        
        # Average sentence length (optimal around 15-20 words)
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        length_score = 1.0 - abs(avg_sentence_length - 17.5) / 17.5
        length_score = max(0.0, min(1.0, length_score))
        
        # Check for common clarity issues
        issues = 0
        if any(len(s.split()) > 40 for s in sentences):  # Very long sentences
            issues += 1
        if any(len(s.split()) < 3 for s in sentences):  # Very short sentences
            issues += 1
        
        issue_penalty = issues * 0.1
        clarity = max(0.0, length_score - issue_penalty)
        
        return clarity
    
    def calculate_completeness(self, summary: str, original: str, key_topics: Optional[List[str]] = None) -> float:
        """
        Calculate completeness score (0-1)
        
        Args:
            summary: Generated summary
            original: Original text
            key_topics: Optional list of key topics to check for
        
        Returns:
            Completeness score
        """
        if not summary or not original:
            return 0.0
        
        # Simple approach: check coverage of important terms
        original_words = set(original.lower().split())
        summary_words = set(summary.lower().split())
        
        # Calculate overlap
        if not original_words:
            return 0.0
        
        overlap = len(original_words & summary_words)
        coverage = overlap / len(original_words)
        
        # Boost score if key topics are present
        if key_topics:
            topics_covered = sum(1 for topic in key_topics if topic.lower() in summary.lower())
            topic_bonus = topics_covered / len(key_topics) * 0.2
            coverage = min(1.0, coverage + topic_bonus)
        
        return coverage
    
    def calculate_citation_accuracy(self, citations: List[Dict], document: Dict) -> float:
        """
        Calculate citation accuracy (0-1)
        
        Args:
            citations: List of citations
            document: Document dictionary with page information
        
        Returns:
            Citation accuracy score
        """
        if not citations:
            return 0.0
        
        # Check if cited pages exist in document
        pages_metadata = document.get("metadata", {}).get("pages", [])
        valid_pages = {page["page"] for page in pages_metadata if page.get("has_text", False)}
        
        if not valid_pages:
            return 0.5  # Can't verify, give neutral score
        
        valid_citations = sum(1 for cit in citations if cit.get("page", 0) in valid_pages)
        accuracy = valid_citations / len(citations) if citations else 0.0
        
        return accuracy

