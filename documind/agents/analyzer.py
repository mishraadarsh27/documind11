"""
Analyzer Agent - Produces three summary types: executive, bullet, and TL;DR
"""

from typing import Dict, Optional
from openai import OpenAI
from loguru import logger
import os


class AnalyzerAgent:
    """
    Analyzer Agent generates multiple summary types:
    - Executive summary: High-level overview for decision-makers
    - Bullet-point summary: Structured key points
    - TL;DR summary: Very brief summary
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize Analyzer Agent
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    
    def generate_summaries(self, document: Dict, custom_instructions: Optional[Dict] = None) -> Dict:
        """
        Generate all three summary types
        
        Args:
            document: Document dictionary from Reader Agent
            custom_instructions: Optional custom instructions for summaries
        
        Returns:
            Dictionary with all summary types
        """
        text = document.get("text", "")
        metadata = document.get("metadata", {})
        
        summaries = {
            "executive": self.generate_executive_summary(text, metadata, custom_instructions),
            "bullet": self.generate_bullet_summary(text, metadata, custom_instructions),
            "tldr": self.generate_tldr_summary(text, metadata, custom_instructions)
        }
        
        return summaries
    
    def generate_executive_summary(self, text: str, metadata: Dict, custom_instructions: Optional[Dict] = None) -> str:
        """
        Generate executive summary
        
        Args:
            text: Document text
            metadata: Document metadata
            custom_instructions: Optional custom instructions
        
        Returns:
            Executive summary text
        """
        prompt = self._build_executive_prompt(text, metadata, custom_instructions)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating concise executive summaries for business documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return "Error generating executive summary."
    
    def generate_bullet_summary(self, text: str, metadata: Dict, custom_instructions: Optional[Dict] = None) -> str:
        """
        Generate bullet-point summary
        
        Args:
            text: Document text
            metadata: Document metadata
            custom_instructions: Optional custom instructions
        
        Returns:
            Bullet-point summary text
        """
        prompt = self._build_bullet_prompt(text, metadata, custom_instructions)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating structured bullet-point summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating bullet summary: {e}")
            return "Error generating bullet summary."
    
    def generate_tldr_summary(self, text: str, metadata: Dict, custom_instructions: Optional[Dict] = None) -> str:
        """
        Generate TL;DR summary
        
        Args:
            text: Document text
            metadata: Document metadata
            custom_instructions: Optional custom instructions
        
        Returns:
            TL;DR summary text
        """
        prompt = self._build_tldr_prompt(text, metadata, custom_instructions)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating very brief TL;DR summaries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating TL;DR summary: {e}")
            return "Error generating TL;DR summary."
    
    def _build_executive_prompt(self, text: str, metadata: Dict, custom_instructions: Optional[Dict] = None) -> str:
        """Build prompt for executive summary"""
        source_info = f"Document: {metadata.get('source', 'Unknown')}"
        if metadata.get('total_pages'):
            source_info += f" ({metadata['total_pages']} pages)"
        
        instructions = custom_instructions.get("executive", "") if custom_instructions else ""
        
        prompt = f"""Create a comprehensive executive summary for the following document.

{source_info}

The executive summary should:
- Provide a high-level overview suitable for decision-makers
- Highlight key findings, recommendations, and implications
- Be clear, concise, and actionable
- Focus on strategic insights rather than details

{instructions}

Document content:
{text[:15000]}  # Limit to avoid token limits

Executive Summary:"""
        return prompt
    
    def _build_bullet_prompt(self, text: str, metadata: Dict, custom_instructions: Optional[Dict] = None) -> str:
        """Build prompt for bullet summary"""
        source_info = f"Document: {metadata.get('source', 'Unknown')}"
        
        instructions = custom_instructions.get("bullet", "") if custom_instructions else ""
        
        prompt = f"""Create a structured bullet-point summary of the following document.

{source_info}

The summary should:
- Use clear bullet points with proper hierarchy
- Cover all major topics and sections
- Be well-organized and easy to scan
- Include key facts, figures, and conclusions

{instructions}

Document content:
{text[:15000]}

Bullet-Point Summary:"""
        return prompt
    
    def _build_tldr_prompt(self, text: str, metadata: Dict, custom_instructions: Optional[Dict] = None) -> str:
        """Build prompt for TL;DR summary"""
        source_info = f"Document: {metadata.get('source', 'Unknown')}"
        
        instructions = custom_instructions.get("tldr", "") if custom_instructions else ""
        
        prompt = f"""Create a very brief TL;DR (Too Long; Didn't Read) summary of the following document.

{source_info}

The TL;DR should:
- Be extremely concise (2-3 sentences maximum)
- Capture the essence and main point
- Be suitable for quick understanding

{instructions}

Document content:
{text[:15000]}

TL;DR:"""
        return prompt

