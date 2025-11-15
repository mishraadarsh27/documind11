"""OCR Processing Utilities"""

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from typing import Optional
from loguru import logger
import os


class OCRProcessor:
    """OCR processing for scanned documents"""
    
    def __init__(self, tesseract_cmd: Optional[str] = None, language: str = "eng"):
        """
        Initialize OCR processor
        
        Args:
            tesseract_cmd: Path to tesseract executable
            language: OCR language code
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        self.language = language
    
    def ocr_page(self, pdf_path: str, page_num: int) -> str:
        """
        Perform OCR on a specific PDF page
        
        Args:
            pdf_path: Path to PDF file
            page_num: Page number (1-indexed)
        
        Returns:
            Extracted text
        """
        try:
            # Convert PDF page to image
            images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num)
            if images:
                image = images[0]
                # Perform OCR
                text = pytesseract.image_to_string(image, lang=self.language)
                return text
            return ""
        except Exception as e:
            logger.error(f"Error performing OCR on page {page_num}: {e}")
            return ""
    
    def ocr_image(self, image_path: str) -> str:
        """Perform OCR on an image file"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=self.language)
            return text
        except Exception as e:
            logger.error(f"Error performing OCR on image: {e}")
            return ""

