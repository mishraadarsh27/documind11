"""PDF Parsing Utilities"""

import pdfplumber
import PyPDF2
from typing import List, Dict
from loguru import logger


class PDFParser:
    """Utility class for PDF parsing operations"""
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
        return text
    
    def get_metadata(self, pdf_path: str) -> Dict:
        """Extract PDF metadata"""
        try:
            with open(pdf_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                metadata = pdf_reader.metadata or {}
                return {
                    "title": metadata.get("/Title", ""),
                    "author": metadata.get("/Author", ""),
                    "subject": metadata.get("/Subject", ""),
                    "creator": metadata.get("/Creator", ""),
                    "producer": metadata.get("/Producer", ""),
                    "num_pages": len(pdf_reader.pages)
                }
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {}

