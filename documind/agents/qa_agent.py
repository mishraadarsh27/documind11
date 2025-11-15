"""
Q&A Agent - Performs retrieval-augmented question answering with citations
Uses FREE models - No API key required!
"""

from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from loguru import logger
import os
import hashlib
import re


class QAAgent:
    """
    Q&A Agent performs retrieval-augmented generation (RAG) for question answering
    with page-level citations and confidence scoring
    Uses FREE sentence transformers - No OpenAI API required!
    """
    
    def __init__(self):
        """
        Initialize Q&A Agent with FREE models
        """
        # Initialize embedding model (FREE - no API key needed)
        try:
            logger.info("Loading FREE embedding model: all-MiniLM-L6-v2")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embedding model loaded successfully!")
        except Exception as e:
            logger.warning(f"Could not load embedding model: {e}")
            self.embedding_model = None
        
        # Initialize vector store
        self.vector_store = None
        self.collection = None
    
    def setup_document(self, document: Dict, collection_name: Optional[str] = None):
        """
        Set up document for Q&A by creating vector embeddings
        
        Args:
            document: Document dictionary from Reader Agent
            collection_name: Name for the vector store collection
        """
        if not self.embedding_model:
            logger.warning("Embedding model not available. Q&A may have limited functionality.")
            return
        
        chunks = document.get("chunks", [])
        if not chunks:
            logger.warning("No chunks found in document.")
            return
        
        # Initialize ChromaDB
        try:
            self.vector_store = chromadb.Client(Settings(anonymized_telemetry=False))
            
            # Create or get collection
            doc_id = hashlib.md5(document.get("metadata", {}).get("source", "").encode()).hexdigest()
            collection_name = collection_name or f"documind_{doc_id[:8]}"
            
            try:
                self.collection = self.vector_store.get_collection(collection_name)
                logger.info(f"Using existing collection: {collection_name}")
            except:
                self.collection = self.vector_store.create_collection(collection_name)
                logger.info(f"Created new collection: {collection_name}")
            
            # Add chunks to vector store
            texts = [chunk.get("text", "") for chunk in chunks]
            embeddings = self.embedding_model.encode(texts).tolist()
            
            ids = [f"chunk_{i}" for i in range(len(chunks))]
            metadatas = [
                {
                    "page": chunk.get("page", 0),
                    "chunk_index": chunk.get("chunk_index", i),
                    "char_count": chunk.get("char_count", 0)
                }
                for i, chunk in enumerate(chunks)
            ]
            
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                ids=ids,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(chunks)} chunks to vector store")
            
        except Exception as e:
            logger.error(f"Error setting up vector store: {e}")
            self.vector_store = None
    
    def answer(self, question: str, top_k: int = 3, return_citations: bool = True) -> Dict:
        """
        Answer a question about the document using FREE extractive Q&A
        
        Args:
            question: User question
            top_k: Number of relevant chunks to retrieve
            return_citations: Whether to include page citations
        
        Returns:
            Dictionary with answer, citations, and confidence
        """
        if not self.collection:
            return {
                "answer": "Document not set up for Q&A. Please call setup_document first.",
                "citations": [],
                "confidence": 0.0
            }
        
        # Retrieve relevant chunks
        relevant_chunks = self._retrieve_relevant_chunks(question, top_k)
        
        if not relevant_chunks:
            return {
                "answer": "I couldn't find relevant information to answer your question in the document.",
                "citations": [],
                "confidence": 0.0
            }
        
        # Generate answer using extractive method (FREE - no API needed)
        answer = self._generate_extractive_answer(question, relevant_chunks)
        
        # Extract citations
        citations = []
        if return_citations:
            for chunk in relevant_chunks:
                page = chunk.get("page", 0)
                if page > 0:
                    citations.append({
                        "page": page,
                        "text": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"]
                    })
        
        # Calculate confidence
        confidence = self._calculate_confidence(question, answer, relevant_chunks)
        
        return {
            "answer": answer,
            "citations": citations,
            "confidence": confidence,
            "relevant_chunks": len(relevant_chunks)
        }
    
    def _retrieve_relevant_chunks(self, question: str, top_k: int) -> List[Dict]:
        """Retrieve relevant chunks using vector similarity"""
        try:
            # Generate question embedding
            question_embedding = self.embedding_model.encode([question]).tolist()[0]
            
            # Query vector store
            results = self.collection.query(
                query_embeddings=[question_embedding],
                n_results=top_k
            )
            
            # Format results
            chunks = []
            if results["documents"] and len(results["documents"][0]) > 0:
                for i, doc in enumerate(results["documents"][0]):
                    chunk = {
                        "text": doc,
                        "page": results["metadatas"][0][i].get("page", 0),
                        "chunk_index": results["metadatas"][0][i].get("chunk_index", 0),
                        "distance": results["distances"][0][i] if "distances" in results else 0.0
                    }
                    chunks.append(chunk)
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error retrieving chunks: {e}")
            return []
    
    def _generate_extractive_answer(self, question: str, chunks: List[Dict]) -> str:
        """
        Generate answer using extractive method (FREE - no API needed)
        Finds the most relevant sentence from chunks
        """
        try:
            # Combine all chunk texts
            context = "\n\n".join([chunk["text"] for chunk in chunks])
            
            # Simple extractive approach: find sentences that contain question keywords
            question_keywords = set(word.lower() for word in question.split() if len(word) > 3)
            
            # Split into sentences
            import nltk
            try:
                nltk.download('punkt', quiet=True)
            except:
                pass
            from nltk.tokenize import sent_tokenize
            
            sentences = sent_tokenize(context)
            
            # Score sentences based on keyword matches
            scored_sentences = []
            for sentence in sentences:
                sentence_lower = sentence.lower()
                matches = sum(1 for keyword in question_keywords if keyword in sentence_lower)
                score = matches / len(question_keywords) if question_keywords else 0
                scored_sentences.append((sentence, score))
            
            # Get top sentences
            scored_sentences.sort(key=lambda x: x[1], reverse=True)
            top_sentences = [s for s, score in scored_sentences[:3] if score > 0]
            
            if top_sentences:
                # Combine top sentences
                answer = " ".join(top_sentences)
                # Clean up
                answer = re.sub(r'\s+', ' ', answer).strip()
                return answer
            else:
                # Fallback: return first chunk
                return chunks[0]["text"][:500] if chunks else "I couldn't find a specific answer to your question."
                
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            # Fallback
            if chunks:
                return chunks[0]["text"][:500]
            return "Error generating answer."
    
    def _calculate_confidence(self, question: str, answer: str, chunks: List[Dict]) -> float:
        """Calculate confidence score (0-1)"""
        if not chunks:
            return 0.0
        
        base_confidence = 0.5
        
        # Adjust based on number of chunks
        if len(chunks) >= 2:
            base_confidence += 0.2
        elif len(chunks) == 1:
            base_confidence += 0.1
        
        # Adjust based on distances (if available)
        if chunks and "distance" in chunks[0]:
            avg_distance = sum(c.get("distance", 1.0) for c in chunks) / len(chunks)
            # Lower distance = higher confidence
            distance_confidence = max(0, 1.0 - avg_distance)
            base_confidence = (base_confidence + distance_confidence) / 2
        
        # Adjust based on answer quality
        if len(answer) > 50:
            base_confidence += 0.1
        
        return min(1.0, base_confidence)
