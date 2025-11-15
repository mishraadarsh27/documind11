"""Document Chunking Utilities"""

from typing import List, Dict, Optional
import re
from loguru import logger


class DocumentChunker:
    """Utility for chunking documents with metadata"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize chunker
        
        Args:
            chunk_size: Target chunk size in characters
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> List[Dict]:
        """
        Chunk text into smaller pieces
        
        Args:
            text: Input text
        
        Returns:
            List of chunks with metadata
        """
        chunks = []
        words = text.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    "text": chunk_text,
                    "char_count": len(chunk_text),
                    "word_count": len(current_chunk),
                    "chunk_index": len(chunks)
                })
                
                # Start new chunk with overlap
                overlap_words = current_chunk[-self.chunk_overlap//10:] if len(current_chunk) > self.chunk_overlap//10 else []
                current_chunk = overlap_words + [word]
                current_length = sum(len(w) + 1 for w in current_chunk)
            else:
                current_chunk.append(word)
                current_length += word_length
        
        # Add final chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "char_count": len(chunk_text),
                "word_count": len(current_chunk),
                "chunk_index": len(chunks)
            })
        
        return chunks
    
    def chunk_with_pages(self, text: str, pages_metadata: List[Dict]) -> List[Dict]:
        """
        Chunk text while preserving page references
        
        Args:
            text: Full text
            pages_metadata: Metadata for each page
        
        Returns:
            List of chunks with page references
        """
        # Split text by pages first
        page_texts = []
        current_page = 1
        page_start = 0
        
        for page_meta in pages_metadata:
            page_num = page_meta["page"]
            page_length = page_meta["char_count"]
            
            if page_num > current_page:
                # Extract text for previous pages
                page_text = text[page_start:page_start + page_length]
                page_texts.append({
                    "page": current_page,
                    "text": page_text
                })
                page_start += page_length
                current_page = page_num
        
        # Add last page
        if page_start < len(text):
            page_texts.append({
                "page": current_page,
                "text": text[page_start:]
            })
        
        # Now chunk each page section
        chunks = []
        for page_data in page_texts:
            page_chunks = self.chunk_text(page_data["text"])
            for chunk in page_chunks:
                chunk["page"] = page_data["page"]
                chunks.append(chunk)
        
        return chunks

