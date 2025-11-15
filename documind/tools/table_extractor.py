"""Table Extraction Utilities"""

import pdfplumber
import pandas as pd
from typing import List, Dict, Optional
from loguru import logger
import json


class TableExtractor:
    """Utility for extracting and formatting tables from documents"""
    
    def extract_tables_from_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Extract all tables from PDF
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            List of table dictionaries
        """
        tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_tables = page.extract_tables()
                    for table_idx, table in enumerate(page_tables):
                        if table and len(table) > 1:  # At least header + one row
                            # Convert to structured format
                            structured_table = self._structure_table(table)
                            tables.append({
                                "page": page_num,
                                "table_index": table_idx,
                                "data": structured_table,
                                "rows": len(table),
                                "cols": len(table[0]) if table else 0,
                                "format": "json"
                            })
        except Exception as e:
            logger.error(f"Error extracting tables: {e}")
        
        return tables
    
    def _structure_table(self, table: List[List]) -> Dict:
        """
        Structure table data
        
        Args:
            table: Raw table data
        
        Returns:
            Structured table dictionary
        """
        if not table:
            return {}
        
        # First row as headers
        headers = [str(cell).strip() if cell else f"Column_{i}" 
                  for i, cell in enumerate(table[0])]
        
        # Remaining rows as data
        rows = []
        for row in table[1:]:
            row_data = {}
            for i, cell in enumerate(row):
                header = headers[i] if i < len(headers) else f"Column_{i}"
                row_data[header] = str(cell).strip() if cell else ""
            rows.append(row_data)
        
        return {
            "headers": headers,
            "rows": rows
        }
    
    def table_to_csv(self, table: Dict) -> str:
        """Convert table to CSV format"""
        try:
            df = pd.DataFrame(table["rows"])
            return df.to_csv(index=False)
        except Exception as e:
            logger.error(f"Error converting table to CSV: {e}")
            return ""
    
    def table_to_json(self, table: Dict) -> str:
        """Convert table to JSON format"""
        try:
            return json.dumps(table, indent=2)
        except Exception as e:
            logger.error(f"Error converting table to JSON: {e}")
            return "{}"

