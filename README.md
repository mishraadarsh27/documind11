# DocuMind – AI Document Intelligence Agent

**Track: Enterprise Agents**

## Overview

DocuMind is an AI-powered multi-agent system designed to automate the analysis of enterprise documents and convert unstructured text into actionable, well-organized insights. The agent processes PDFs, reports, policy documents, technical manuals, and web-based content, delivering high-quality summaries, structured extractions, and source-grounded answers.

## Features

- **Multi-Format Support**: PDFs, text files, and web URLs
- **Intelligent Extraction**: Tables, dates, metrics, named entities, and action items
- **Multiple Summary Types**: Executive, bullet-point, and TL;DR summaries
- **Question Answering**: RAG-based Q&A with page-level citations
- **Long-Term Memory**: Stores insights for future sessions
- **Quality Evaluation**: Automated assessment of outputs

## System Architecture

DocuMind consists of six specialized agents:

1. **Reader Agent**: Extracts text from PDFs, web pages, and scanned documents with OCR
2. **Extractor Agent**: Identifies tables, numerical values, dates, tasks, and named entities
3. **Analyzer Agent**: Produces three summary types (executive, bullet, TL;DR)
4. **Q&A Agent**: Performs retrieval-augmented question answering with citations
5. **Memory Agent**: Stores extracted insights for future sessions
6. **Evaluator Agent**: Assesses output quality and provides improvement suggestions

## Installation

### Prerequisites

- Python 3.9+
- Tesseract OCR (for OCR functionality)
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt-get install tesseract-ocr`
  - Mac: `brew install tesseract`

### Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd documind
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download spaCy language model**:
```bash
python -m spacy download en_core_web_sm
```

5. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your-api-key-here
```

## 🌐 Web Application

DocuMind includes a **fully functional web application**! 

**Quick Start:**
```bash
cd webapp
pip install -r requirements.txt
export OPENAI_API_KEY=your-key
python app.py
```

Then open: **http://localhost:5000**

**Deploy to Heroku/Railway/Render:** See [WEBAPP_README.md](WEBAPP_README.md) for detailed deployment instructions.

## Quick Start

### Basic Usage

```python
from documind import DocuMind

# Initialize DocuMind
dm = DocuMind(api_key="your-openai-api-key")

# Process a document
result = dm.process_document(
    source="path/to/document.pdf",
    tasks=["extract", "summarize", "qa"]
)

# Access results
print(result.summaries["executive"])
print(result.extractions["tables"])
print(result.qa.answer("What is the main objective?"))
```

### Command Line Interface

```bash
# Process a PDF
python -m documind.cli process document.pdf --tasks extract summarize

# Ask questions
python -m documind.cli qa document.pdf "What are the key findings?"

# Generate summary
python -m documind.cli summarize document.pdf --type executive
```

## Project Structure

```
documind/
├── documind/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── reader.py          # Reader Agent
│   │   ├── extractor.py       # Extractor Agent
│   │   ├── analyzer.py        # Analyzer Agent
│   │   ├── qa_agent.py        # Q&A Agent
│   │   ├── memory.py           # Memory Agent
│   │   └── evaluator.py       # Evaluator Agent
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py      # PDF parsing utilities
│   │   ├── ocr.py             # OCR functionality
│   │   ├── table_extractor.py # Table extraction
│   │   └── chunker.py         # Document chunking
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── memory_bank.py     # Long-term memory
│   │   └── session_memory.py   # Session memory
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py         # Evaluation metrics
│   │   └── evaluator.py       # Quality assessment
│   ├── __init__.py
│   └── orchestrator.py        # Main orchestrator
├── notebooks/
│   └── documind_demo.ipynb    # Kaggle notebook
├── examples/
│   └── sample_documents/      # Example documents
├── tests/
│   └── test_agents.py         # Unit tests
├── requirements.txt
├── .env.example
└── README.md
```

## Usage Examples

### Example 1: Extract Tables and Metrics

```python
from documind import DocuMind

dm = DocuMind()
result = dm.process_document("financial_report.pdf")

# Access extracted tables
for table in result.extractions["tables"]:
    print(f"Table on page {table['page']}:")
    print(table['data'])

# Access metrics
print("Key Metrics:", result.extractions["metrics"])
```

### Example 2: Generate Summaries

```python
result = dm.process_document("policy_document.pdf")

# Executive summary
print(result.summaries["executive"])

# Bullet-point summary
print(result.summaries["bullet"])

# TL;DR summary
print(result.summaries["tldr"])
```

### Example 3: Question Answering

```python
# Process document first
result = dm.process_document("technical_manual.pdf")

# Ask questions
answer = result.qa.answer(
    "What are the system requirements?",
    return_citations=True
)

print(f"Answer: {answer['answer']}")
print(f"Citations: {answer['citations']}")
```

### Example 4: Memory and Persistence

```python
# Store insights in memory
dm.memory.store_insights(
    document_id="doc_123",
    insights=result.extractions
)

# Retrieve from memory in future session
insights = dm.memory.retrieve_insights("doc_123")
```

## Evaluation

DocuMind includes built-in evaluation capabilities:

```python
# Evaluate summary quality
evaluation = dm.evaluator.evaluate_summary(
    summary=result.summaries["executive"],
    reference=original_text
)

print(f"ROUGE Score: {evaluation['rouge']}")
print(f"Clarity: {evaluation['clarity']}")
print(f"Completeness: {evaluation['completeness']}")
```

## Long-Running Operations

DocuMind supports pausing and resuming operations:

```python
# Process with pause points
result = dm.process_document(
    "large_document.pdf",
    pause_after=["extraction", "summarization"]
)

# Resume from checkpoint
result = dm.resume_from_checkpoint("checkpoint_123")
```

## API Reference

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API reference.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License.

## Acknowledgments

- OpenAI for language models
- LangChain for agent framework
- spaCy for NLP capabilities
- Community contributors

