# DocuMind API Documentation

## DocuMind Class

Main orchestrator class for document processing.

### Initialization

```python
DocuMind(
    api_key: Optional[str] = None,
    ocr_enabled: bool = True,
    memory_enabled: bool = True,
    evaluation_enabled: bool = True,
    storage_path: str = "./memory_bank"
)
```

**Parameters:**
- `api_key`: OpenAI API key (or set OPENAI_API_KEY env var)
- `ocr_enabled`: Enable OCR for scanned documents
- `memory_enabled`: Enable memory system
- `evaluation_enabled`: Enable evaluation
- `storage_path`: Path for memory storage

### Methods

#### `process_document(source, tasks=None, document_id=None, store_in_memory=True)`

Process a document with specified tasks.

**Parameters:**
- `source`: Path to document or URL
- `tasks`: List of tasks (`extract`, `summarize`, `qa`, `evaluate`)
- `document_id`: Optional document identifier
- `store_in_memory`: Whether to store in memory

**Returns:** Dictionary with results

**Example:**
```python
result = dm.process_document(
    source="document.pdf",
    tasks=["extract", "summarize"]
)
```

#### `answer_question(question, return_citations=True)`

Answer a question about the current document.

**Parameters:**
- `question`: User question
- `return_citations`: Include page citations

**Returns:** Dictionary with answer, citations, confidence

**Example:**
```python
answer = dm.answer_question("What are the key findings?")
```

#### `get_summary(summary_type="executive")`

Get a specific summary type.

**Parameters:**
- `summary_type`: `executive`, `bullet`, or `tldr`

**Returns:** Summary text or None

#### `get_extractions()`

Get extracted information from current document.

**Returns:** Dictionary with extractions or None

#### `search_memory(query, limit=10)`

Search across stored insights.

**Parameters:**
- `query`: Search query
- `limit`: Maximum results

**Returns:** List of matching insights

## Agent Classes

### ReaderAgent

Handles document ingestion.

**Methods:**
- `read_document(source, source_type=None)`: Read document
- `extract_tables_from_pdf(pdf_path)`: Extract tables

### ExtractorAgent

Extracts structured information.

**Methods:**
- `extract_all(document)`: Extract all information types
- `extract_metrics(text)`: Extract numerical metrics
- `extract_dates(text)`: Extract dates
- `extract_tasks(text)`: Extract action items
- `extract_entities(text)`: Extract named entities

### AnalyzerAgent

Generates summaries.

**Methods:**
- `generate_summaries(document, custom_instructions=None)`: Generate all summaries
- `generate_executive_summary(text, metadata, custom_instructions=None)`: Executive summary
- `generate_bullet_summary(text, metadata, custom_instructions=None)`: Bullet summary
- `generate_tldr_summary(text, metadata, custom_instructions=None)`: TL;DR summary

### QAAgent

Question answering with RAG.

**Methods:**
- `setup_document(document, collection_name=None)`: Set up document for Q&A
- `answer(question, top_k=3, return_citations=True)`: Answer question

### MemoryAgent

Manages memory.

**Methods:**
- `store_insights(document_id, insights, metadata=None, persist=True)`: Store insights
- `retrieve_insights(document_id, from_long_term=True)`: Retrieve insights
- `search_insights(query, limit=10)`: Search insights

### EvaluatorAgent

Quality assessment.

**Methods:**
- `evaluate_summary(summary, reference, summary_type="executive")`: Evaluate summary
- `evaluate_extractions(extractions, document)`: Evaluate extractions
- `evaluate_qa(qa_result, document)`: Evaluate Q&A

## Result Structure

### Process Document Result

```python
{
    "document_id": str,
    "document": {
        "text": str,
        "metadata": dict,
        "chunks": list
    },
    "extractions": {
        "tables": list,
        "metrics": list,
        "dates": list,
        "tasks": list,
        "entities": dict
    },
    "summaries": {
        "executive": str,
        "bullet": str,
        "tldr": str
    },
    "qa": QAAgent instance,
    "evaluations": dict,
    "metadata": dict
}
```

### Q&A Answer Result

```python
{
    "answer": str,
    "citations": [
        {
            "page": int,
            "text": str
        }
    ],
    "confidence": float,
    "relevant_chunks": int
}
```

### Evaluation Result

```python
{
    "overall_score": float,
    "clarity": float,
    "completeness": float,
    "rouge_scores": dict,
    "suggestions": list
}
```

