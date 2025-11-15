"""
Memory Bank - Long-term memory storage for insights
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from loguru import logger
import hashlib


class MemoryBank:
    """
    Memory Bank stores extracted insights for long-term persistence
    across multiple sessions
    """
    
    def __init__(self, storage_path: str = "./memory_bank"):
        """
        Initialize Memory Bank
        
        Args:
            storage_path: Path to store memory files
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.storage_path / "memory.json"
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict:
        """Load memory from disk"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading memory: {e}")
                return {}
        return {}
    
    def _save_memory(self):
        """Save memory to disk"""
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def store_insights(self, document_id: str, insights: Dict, metadata: Optional[Dict] = None):
        """
        Store insights for a document
        
        Args:
            document_id: Unique document identifier
            insights: Extracted insights dictionary
            metadata: Optional metadata about the document
        """
        if document_id not in self.memory:
            self.memory[document_id] = {
                "insights": {},
                "metadata": metadata or {},
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        
        # Store insights
        self.memory[document_id]["insights"] = insights
        self.memory[document_id]["updated_at"] = datetime.now().isoformat()
        
        if metadata:
            self.memory[document_id]["metadata"].update(metadata)
        
        self._save_memory()
        logger.info(f"Stored insights for document: {document_id}")
    
    def retrieve_insights(self, document_id: str) -> Optional[Dict]:
        """
        Retrieve stored insights for a document
        
        Args:
            document_id: Document identifier
        
        Returns:
            Stored insights or None
        """
        return self.memory.get(document_id)
    
    def search_insights(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search across all stored insights
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            List of matching insights
        """
        results = []
        query_lower = query.lower()
        
        for doc_id, data in self.memory.items():
            insights = data.get("insights", {})
            
            # Simple text search
            insights_str = json.dumps(insights).lower()
            if query_lower in insights_str:
                results.append({
                    "document_id": doc_id,
                    "insights": insights,
                    "metadata": data.get("metadata", {}),
                    "relevance": insights_str.count(query_lower)  # Simple relevance score
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:limit]
    
    def get_all_documents(self) -> List[str]:
        """Get list of all document IDs in memory"""
        return list(self.memory.keys())
    
    def delete_document(self, document_id: str):
        """Delete insights for a document"""
        if document_id in self.memory:
            del self.memory[document_id]
            self._save_memory()
            logger.info(f"Deleted insights for document: {document_id}")
    
    def compact_memory(self, max_age_days: int = 90):
        """
        Compact memory by removing old entries
        
        Args:
            max_age_days: Maximum age in days before removal
        """
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        to_remove = []
        for doc_id, data in self.memory.items():
            updated_at = datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
            if updated_at < cutoff_date:
                to_remove.append(doc_id)
        
        for doc_id in to_remove:
            del self.memory[doc_id]
        
        if to_remove:
            self._save_memory()
            logger.info(f"Compacted memory: removed {len(to_remove)} old entries")

