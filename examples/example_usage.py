"""
Example usage of DocuMind
"""

import os
from documind import DocuMind

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'your-api-key-here'

# Initialize DocuMind
dm = DocuMind(
    api_key=os.getenv('OPENAI_API_KEY'),
    ocr_enabled=True,
    memory_enabled=True,
    evaluation_enabled=True
)

# Example 1: Process a PDF document
print("Example 1: Processing PDF document")
result = dm.process_document(
    source="sample_document.pdf",
    tasks=["extract", "summarize", "evaluate"],
    store_in_memory=True
)

print(f"Document ID: {result['document_id']}")
print(f"Total pages: {result['document']['metadata'].get('total_pages', 'N/A')}")

# Example 2: View extractions
print("\nExample 2: Viewing extractions")
extractions = result['extractions']
print(f"Tables: {len(extractions.get('tables', []))}")
print(f"Metrics: {len(extractions.get('metrics', []))}")
print(f"Dates: {len(extractions.get('dates', []))}")

# Example 3: View summaries
print("\nExample 3: Viewing summaries")
summaries = result['summaries']
print("Executive Summary:")
print(summaries.get('executive', 'N/A')[:200] + "...")

# Example 4: Question Answering
print("\nExample 4: Question Answering")
result = dm.process_document(
    source="sample_document.pdf",
    tasks=["qa"]
)

answer = dm.answer_question("What is the main objective?", return_citations=True)
print(f"Q: What is the main objective?")
print(f"A: {answer['answer']}")
print(f"Confidence: {answer['confidence']:.2f}")

# Example 5: Process URL
print("\nExample 5: Processing URL")
result = dm.process_document(
    source="https://example.com/article",
    tasks=["extract", "summarize"]
)
print(f"Processed: {result['document']['metadata']['source']}")

# Example 6: Memory Search
print("\nExample 6: Memory Search")
search_results = dm.search_memory("financial", limit=5)
print(f"Found {len(search_results)} results")

