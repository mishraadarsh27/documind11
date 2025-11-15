"""
Session Memory - In-memory storage for active session context
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from loguru import logger


class SessionMemory:
    """
    Session Memory maintains context during an active user session
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize Session Memory
        
        Args:
            session_id: Optional session identifier
        """
        self.session_id = session_id or f"session_{datetime.now().timestamp()}"
        self.context = {
            "documents": {},
            "conversation_history": [],
            "current_document": None,
            "extractions": {},
            "summaries": {},
            "qa_history": []
        }
        self.created_at = datetime.now()
    
    def add_document(self, document_id: str, document: Dict):
        """Add document to session context"""
        self.context["documents"][document_id] = document
        self.context["current_document"] = document_id
        logger.info(f"Added document {document_id} to session {self.session_id}")
    
    def store_extractions(self, document_id: str, extractions: Dict):
        """Store extractions for a document"""
        if document_id not in self.context["extractions"]:
            self.context["extractions"][document_id] = {}
        self.context["extractions"][document_id].update(extractions)
    
    def store_summaries(self, document_id: str, summaries: Dict):
        """Store summaries for a document"""
        if document_id not in self.context["summaries"]:
            self.context["summaries"][document_id] = {}
        self.context["summaries"][document_id].update(summaries)
    
    def add_qa_pair(self, question: str, answer: Dict):
        """Add Q&A pair to history"""
        self.context["qa_history"].append({
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_conversation(self, role: str, content: str):
        """Add to conversation history"""
        self.context["conversation_history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_context(self) -> Dict:
        """Get full session context"""
        return self.context
    
    def get_current_document(self) -> Optional[Dict]:
        """Get current document"""
        doc_id = self.context.get("current_document")
        if doc_id:
            return self.context["documents"].get(doc_id)
        return None
    
    def clear(self):
        """Clear session memory"""
        self.context = {
            "documents": {},
            "conversation_history": [],
            "current_document": None,
            "extractions": {},
            "summaries": {},
            "qa_history": []
        }
        logger.info(f"Cleared session memory for {self.session_id}")

