"""
Extractor Agent - Identifies tables, numerical values, dates, tasks, and named entities
"""

import re
from typing import Dict, List, Optional
import dateparser
import spacy
from loguru import logger

from ..tools.table_extractor import TableExtractor


class ExtractorAgent:
    """
    Extractor Agent identifies and extracts structured information:
    - Tables
    - Numerical values and metrics
    - Dates and deadlines
    - Action items and tasks
    - Named entities (people, organizations, locations)
    """
    
    def __init__(self, spacy_model: str = "en_core_web_sm"):
        """
        Initialize Extractor Agent
        
        Args:
            spacy_model: spaCy model name
        """
        try:
            self.nlp = spacy.load(spacy_model)
        except OSError:
            logger.warning(f"spaCy model {spacy_model} not found. Loading small English model.")
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except:
                logger.error("spaCy model not available. Some features may not work.")
                self.nlp = None
        
        self.table_extractor = TableExtractor()
        
        # Patterns for extraction
        self.metric_patterns = [
            r'\$[\d,]+(?:\.\d{2})?',  # Currency
            r'[\d,]+(?:\.\d+)?%',      # Percentages
            r'[\d,]+(?:\.\d+)?\s*(?:million|billion|thousand|M|B|K)',  # Large numbers
            r'\d+\.\d+',                # Decimals
        ]
        
        self.task_patterns = [
            r'(?:action|task|todo|must|should|need to|required to)',
            r'(?:deadline|due date|by|before)',
        ]
    
    def extract_all(self, document: Dict) -> Dict:
        """
        Extract all types of information from document
        
        Args:
            document: Document dictionary from Reader Agent
        
        Returns:
            Dictionary with all extractions
        """
        extractions = {
            "tables": [],
            "metrics": [],
            "dates": [],
            "tasks": [],
            "entities": []
        }
        
        text = document.get("text", "")
        metadata = document.get("metadata", {})
        source = metadata.get("source", "")
        
        # Extract tables if PDF
        if metadata.get("source_type") == "pdf" and source:
            try:
                extractions["tables"] = self.table_extractor.extract_tables_from_pdf(source)
            except Exception as e:
                logger.error(f"Error extracting tables: {e}")
        
        # Extract metrics
        extractions["metrics"] = self.extract_metrics(text)
        
        # Extract dates
        extractions["dates"] = self.extract_dates(text)
        
        # Extract tasks
        extractions["tasks"] = self.extract_tasks(text)
        
        # Extract named entities
        extractions["entities"] = self.extract_entities(text)
        
        return extractions
    
    def extract_metrics(self, text: str) -> List[Dict]:
        """
        Extract numerical metrics from text
        
        Args:
            text: Input text
        
        Returns:
            List of metric dictionaries
        """
        metrics = []
        
        # Find all metric patterns
        for pattern in self.metric_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 50)
                context_end = min(len(text), match.end() + 50)
                context = text[context_start:context_end]
                
                metrics.append({
                    "value": match.group(),
                    "type": self._classify_metric_type(match.group()),
                    "context": context.strip(),
                    "position": match.start()
                })
        
        # Remove duplicates and sort
        unique_metrics = []
        seen = set()
        for metric in metrics:
            key = (metric["value"], metric["position"])
            if key not in seen:
                seen.add(key)
                unique_metrics.append(metric)
        
        return sorted(unique_metrics, key=lambda x: x["position"])
    
    def _classify_metric_type(self, value: str) -> str:
        """Classify metric type"""
        if '$' in value:
            return "currency"
        elif '%' in value:
            return "percentage"
        elif any(term in value.lower() for term in ['million', 'billion', 'thousand', 'm', 'b', 'k']):
            return "large_number"
        elif '.' in value:
            return "decimal"
        else:
            return "integer"
    
    def extract_dates(self, text: str) -> List[Dict]:
        """
        Extract dates from text
        
        Args:
            text: Input text
        
        Returns:
            List of date dictionaries
        """
        dates = []
        
        # Use dateparser to find dates
        # Simple approach: look for date-like patterns
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                date_str = match.group()
                parsed_date = dateparser.parse(date_str)
                
                if parsed_date:
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(text), match.end() + 50)
                    context = text[context_start:context_end]
                    
                    dates.append({
                        "date_string": date_str,
                        "parsed_date": parsed_date.isoformat(),
                        "context": context.strip(),
                        "position": match.start()
                    })
        
        # Remove duplicates
        unique_dates = []
        seen = set()
        for date in dates:
            key = (date["date_string"], date["position"])
            if key not in seen:
                seen.add(key)
                unique_dates.append(date)
        
        return sorted(unique_dates, key=lambda x: x["position"])
    
    def extract_tasks(self, text: str) -> List[Dict]:
        """
        Extract action items and tasks
        
        Args:
            text: Input text
        
        Returns:
            List of task dictionaries
        """
        tasks = []
        
        # Look for task indicators
        task_indicators = [
            r'(?:action|task|todo|must|should|need to|required to).{0,100}',
            r'(?:deadline|due date|by|before).{0,100}',
        ]
        
        for pattern in task_indicators:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                task_text = match.group().strip()
                
                # Extract associated date if present
                date_match = re.search(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', task_text)
                due_date = date_match.group() if date_match else None
                
                tasks.append({
                    "task_text": task_text,
                    "due_date": due_date,
                    "position": match.start()
                })
        
        # Remove duplicates
        unique_tasks = []
        seen = set()
        for task in tasks:
            key = task["task_text"][:50]  # Use first 50 chars as key
            if key not in seen:
                seen.add(key)
                unique_tasks.append(task)
        
        return sorted(unique_tasks, key=lambda x: x["position"])
    
    def extract_entities(self, text: str) -> List[Dict]:
        """
        Extract named entities using spaCy
        
        Args:
            text: Input text
        
        Returns:
            List of entity dictionaries
        """
        if not self.nlp:
            return []
        
        entities = []
        doc = self.nlp(text)
        
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "label_description": spacy.explain(ent.label_),
                "start": ent.start_char,
                "end": ent.end_char
            })
        
        # Group by type
        entities_by_type = {}
        for entity in entities:
            label = entity["label"]
            if label not in entities_by_type:
                entities_by_type[label] = []
            entities_by_type[label].append(entity)
        
        return {
            "all": entities,
            "by_type": entities_by_type
        }

