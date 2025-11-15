"""
Tests for Reader Agent
"""

import pytest
from documind.agents.reader import ReaderAgent


def test_reader_initialization():
    """Test Reader Agent initialization"""
    reader = ReaderAgent(ocr_enabled=False)
    assert reader is not None
    assert reader.ocr_enabled == False


def test_detect_source_type():
    """Test source type detection"""
    reader = ReaderAgent(ocr_enabled=False)
    
    assert reader._detect_source_type("http://example.com") == "url"
    assert reader._detect_source_type("https://example.com") == "url"
    assert reader._detect_source_type("document.pdf") == "pdf"
    assert reader._detect_source_type("document.txt") == "text"


# Note: Full integration tests would require actual document files

