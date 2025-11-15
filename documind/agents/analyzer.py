"""
Analyzer Agent - Produces three summary types: executive, bullet, and TL;DR
Uses FREE Hugging Face models - No API key required!
"""

from typing import Dict, Optional
from transformers import pipeline
from loguru import logger
import os


class AnalyzerAgent:
    """
    Analyzer Agent generates multiple summary types using FREE Hugging Face models:
    - Executive summary: High-level overview for decision-makers
    - Bullet-point summary: Structured key points
    - TL;DR summary: Very brief summary
    """
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize Analyzer Agent with FREE Hugging Face models
        
        Args:
            model_name: Hugging Face model name for summarization
        """
        self.model_name = model_name
        try:
            logger.info(f"Loading FREE summarization model: {model_name}")
            self.summarizer = pipeline("summarization", model=model_name, device=-1)  # device=-1 uses CPU
            logger.info("Summarization model loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading summarization model: {e}")
            logger.info("Falling back to extractive summarization")
            self.summarizer = None
    
    def generate_summaries(self, document: Dict, custom_instructions: Optional[Dict] = None) -> Dict:
        """
        Generate all three summary types
        
        Args:
            document: Document dictionary from Reader Agent
            custom_instructions: Optional custom instructions for summaries (not used with free models)
        
        Returns:
            Dictionary with all summary types
        """
        text = document.get("text", "")
        metadata = document.get("metadata", {})
        
        summaries = {
            "executive": self.generate_executive_summary(text, metadata),
            "bullet": self.generate_bullet_summary(text, metadata),
            "tldr": self.generate_tldr_summary(text, metadata)
        }
        
        return summaries
    
    def generate_executive_summary(self, text: str, metadata: Dict) -> str:
        """
        Generate executive summary using FREE model
        
        Args:
            text: Document text
            metadata: Document metadata
        
        Returns:
            Executive summary text
        """
        if not text or len(text.strip()) < 100:
            return "Document is too short to generate a summary."
        
        try:
            # Chunk text if too long (models have token limits)
            max_length = 1024
            min_length = 100
            
            if len(text) > 5000:
                # Use first part for executive summary
                text_chunk = text[:5000]
            else:
                text_chunk = text
            
            if self.summarizer:
                # Use Hugging Face model
                summary = self.summarizer(
                    text_chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                return summary[0]['summary_text']
            else:
                # Fallback to extractive summary
                return self._extractive_summary(text_chunk, max_sentences=5)
                
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return self._extractive_summary(text[:5000], max_sentences=5)
    
    def generate_bullet_summary(self, text: str, metadata: Dict) -> str:
        """
        Generate bullet-point summary
        
        Args:
            text: Document text
            metadata: Document metadata
        
        Returns:
            Bullet-point summary text
        """
        if not text or len(text.strip()) < 100:
            return "Document is too short to generate a summary."
        
        try:
            # For bullet points, we'll extract key sentences and format them
            import nltk
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
            except:
                pass
            
            from nltk.tokenize import sent_tokenize
            from nltk.corpus import stopwords
            
            # Get sentences
            sentences = sent_tokenize(text[:10000])  # Limit to first 10k chars
            
            # Score sentences (simple TF-IDF-like approach)
            scored_sentences = self._score_sentences(sentences)
            
            # Get top sentences
            top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:10]
            
            # Format as bullets
            bullet_points = []
            for sentence, score in top_sentences:
                bullet_points.append(f"• {sentence.strip()}")
            
            return "\n".join(bullet_points)
            
        except Exception as e:
            logger.error(f"Error generating bullet summary: {e}")
            return "Error generating bullet summary. Please try again."
    
    def generate_tldr_summary(self, text: str, metadata: Dict) -> str:
        """
        Generate TL;DR summary (very brief)
        
        Args:
            text: Document text
            metadata: Document metadata
        
        Returns:
            TL;DR summary text
        """
        if not text or len(text.strip()) < 50:
            return "Document is too short."
        
        try:
            # Use summarizer with very short length
            text_chunk = text[:3000]  # Limit for TL;DR
            
            if self.summarizer:
                summary = self.summarizer(
                    text_chunk,
                    max_length=150,
                    min_length=30,
                    do_sample=False
                )
                return summary[0]['summary_text']
            else:
                # Fallback: first few sentences
                import nltk
                try:
                    nltk.download('punkt', quiet=True)
                except:
                    pass
                from nltk.tokenize import sent_tokenize
                sentences = sent_tokenize(text_chunk)
                return " ".join(sentences[:2])  # First 2 sentences
                
        except Exception as e:
            logger.error(f"Error generating TL;DR summary: {e}")
            # Simple fallback
            return text[:200] + "..." if len(text) > 200 else text
    
    def _extractive_summary(self, text: str, max_sentences: int = 5) -> str:
        """Simple extractive summary as fallback"""
        try:
            import nltk
            try:
                nltk.download('punkt', quiet=True)
            except:
                pass
            from nltk.tokenize import sent_tokenize
            
            sentences = sent_tokenize(text)
            if len(sentences) <= max_sentences:
                return " ".join(sentences)
            
            # Return first and last sentences
            selected = sentences[:max_sentences//2] + sentences[-max_sentences//2:]
            return " ".join(selected)
        except:
            # Ultimate fallback
            words = text.split()
            return " ".join(words[:100]) + "..." if len(words) > 100 else text
    
    def _score_sentences(self, sentences: list) -> list:
        """Score sentences for importance (simple TF-IDF approach)"""
        try:
            from nltk.corpus import stopwords
            from collections import Counter
            
            # Get all words
            all_words = []
            for sentence in sentences:
                words = sentence.lower().split()
                all_words.extend([w for w in words if w.isalnum()])
            
            # Count word frequencies
            word_freq = Counter(all_words)
            
            # Remove stopwords
            try:
                stop_words = set(stopwords.words('english'))
            except:
                stop_words = set()
            
            # Score sentences
            scored = []
            for sentence in sentences:
                words = [w.lower() for w in sentence.split() if w.isalnum() and w.lower() not in stop_words]
                if words:
                    score = sum(word_freq.get(w, 0) for w in words) / len(words)
                    scored.append((sentence, score))
                else:
                    scored.append((sentence, 0))
            
            return scored
        except Exception as e:
            logger.error(f"Error scoring sentences: {e}")
            # Return sentences with equal scores
            return [(s, 1.0) for s in sentences]
