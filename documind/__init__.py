"""
DocuMind - AI Document Intelligence Agent

A multi-agent system for automated document analysis and insight extraction.
"""

__version__ = "1.0.0"
__author__ = "DocuMind Team"

from .orchestrator import DocuMind
from .agents.reader import ReaderAgent
from .agents.extractor import ExtractorAgent
from .agents.analyzer import AnalyzerAgent
from .agents.qa_agent import QAAgent
from .agents.memory import MemoryAgent
from .agents.evaluator import EvaluatorAgent

__all__ = [
    "DocuMind",
    "ReaderAgent",
    "ExtractorAgent",
    "AnalyzerAgent",
    "QAAgent",
    "MemoryAgent",
    "EvaluatorAgent",
]

