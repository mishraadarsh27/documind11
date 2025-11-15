"""
Reader Agent - Extracts text from PDFs, web pages, and scanned documents
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pdfplumber
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from loguru import logger

from ..tools.pdf_parser import PDFParser
from ..tools.ocr import OCRProcessor
from ..tools.chunker import DocumentChunker


class ReaderAgent:
    """
    Reader Agent handles document ingestion from multiple sources:
    - PDF files (text-based and scanned)
    - Text files
    - Web URLs
    - OCR for scanned documents
    """
    
    def __init__(self, ocr_enabled: bool = True, tesseract_cmd: Optional[str] = None):
        """
        Initialize Reader Agent
        
        Args:
            ocr_enabled: Enable OCR for scanned documents
            tesseract_cmd: Path to tesseract executable (if not in PATH)
        """
        self.ocr_enabled = ocr_enabled
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        self.pdf_parser = PDFParser()
        self.ocr_processor = OCRProcessor() if ocr_enabled else None
        self.chunker = DocumentChunker()
        
    def read_document(self, source: str, source_type: Optional[str] = None) -> Dict:
        """
        Read document from various sources
        
        Args:
            source: Path to file or URL
            source_type: Type of source ('pdf', 'text', 'url', 'auto')
        
        Returns:
            Dictionary with text, metadata, and chunks
        """
        if source_type is None:
            source_type = self._detect_source_type(source)
        
        logger.info(f"Reading document from {source_type}: {source}")
        
        if source_type == "pdf":
            return self._read_pdf(source)
        elif source_type == "text":
            return self._read_text(source)
        elif source_type == "url":
            return self._read_url(source)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
    
    def _detect_source_type(self, source: str) -> str:
        """Detect source type from source string"""
        if source.startswith("http://") or source.startswith("https://"):
            return "url"
        elif source.lower().endswith(".pdf"):
            return "pdf"
        elif source.lower().endswith((".txt", ".md", ".text")):
            return "text"
        else:
            # Try to infer from file extension or content
            path = Path(source)
            if path.exists():
                if path.suffix.lower() == ".pdf":
                    return "pdf"
                elif path.suffix.lower() in [".txt", ".md", ".text"]:
                    return "text"
            return "text"  # Default
    
    def _read_pdf(self, pdf_path: str) -> Dict:
        """Read PDF file with OCR fallback for scanned documents"""
        try:
            # Try text extraction first
            text_content = []
            pages_metadata = []
            
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    
                    # If page has no text, try OCR
                    if not page_text or len(page_text.strip()) < 50:
                        if self.ocr_enabled and self.ocr_processor:
                            logger.info(f"Low text content on page {page_num}, attempting OCR")
                            page_text = self.ocr_processor.ocr_page(pdf_path, page_num)
                    
                    if page_text:
                        text_content.append(page_text)
                        pages_metadata.append({
                            "page": page_num,
                            "char_count": len(page_text),
                            "word_count": len(page_text.split()),
                            "has_text": True
                        })
                    else:
                        pages_metadata.append({
                            "page": page_num,
                            "char_count": 0,
                            "word_count": 0,
                            "has_text": False
                        })
            
            full_text = "\n\n".join(text_content)
            
            # Chunk the document with page references
            chunks = self.chunker.chunk_with_pages(full_text, pages_metadata)
            
            return {
                "text": full_text,
                "metadata": {
                    "source": pdf_path,
                    "source_type": "pdf",
                    "total_pages": total_pages,
                    "total_chars": len(full_text),
                    "total_words": len(full_text.split()),
                    "pages": pages_metadata
                },
                "chunks": chunks
            }
            
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_path}: {e}")
            raise
    
    def _read_text(self, text_path: str) -> Dict:
        """Read text file"""
        try:
            with open(text_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            # Simple chunking for text files
            chunks = self.chunker.chunk_text(text)
            
            return {
                "text": text,
                "metadata": {
                    "source": text_path,
                    "source_type": "text",
                    "total_chars": len(text),
                    "total_words": len(text.split()),
                    "lines": text.count("\n")
                },
                "chunks": chunks
            }
        except Exception as e:
            logger.error(f"Error reading text file {text_path}: {e}")
            raise
    
    def _read_url(self, url: str) -> Dict:
        """Read content from URL"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)
            
            # Chunk the content
            chunks = self.chunker.chunk_text(text)
            
            return {
                "text": text,
                "metadata": {
                    "source": url,
                    "source_type": "url",
                    "total_chars": len(text),
                    "total_words": len(text.split()),
                    "title": soup.title.string if soup.title else None
                },
                "chunks": chunks
            }
        except Exception as e:
            logger.error(f"Error reading URL {url}: {e}")
            raise
    
    def extract_tables_from_pdf(self, pdf_path: str) -> List[Dict]:
        """Extract tables from PDF"""
        tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_tables = page.extract_tables()
                    for table_idx, table in enumerate(page_tables):
                        if table:
                            tables.append({
                                "page": page_num,
                                "table_index": table_idx,
                                "data": table,
                                "rows": len(table),
                                "cols": len(table[0]) if table else 0
                            })
        except Exception as e:
            logger.error(f"Error extracting tables from PDF: {e}")
        
        return tables

