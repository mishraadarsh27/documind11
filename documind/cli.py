"""
Command Line Interface for DocuMind
"""

import argparse
import os
import sys
from pathlib import Path

from .orchestrator import DocuMind


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="DocuMind - AI Document Intelligence Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a document with extraction and summarization
  python -m documind.cli process document.pdf --tasks extract summarize
  
  # Ask a question about a document
  python -m documind.cli qa document.pdf "What are the key findings?"
  
  # Generate executive summary
  python -m documind.cli summarize document.pdf --type executive
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process a document')
    process_parser.add_argument('source', help='Path to document or URL')
    process_parser.add_argument('--tasks', nargs='+', 
                              choices=['extract', 'summarize', 'qa', 'evaluate'],
                              default=['extract', 'summarize'],
                              help='Tasks to perform')
    process_parser.add_argument('--api-key', help='OpenAI API key')
    process_parser.add_argument('--no-memory', action='store_true', 
                              help='Disable memory storage')
    process_parser.add_argument('--no-evaluation', action='store_true',
                              help='Disable evaluation')
    
    # Q&A command
    qa_parser = subparsers.add_parser('qa', help='Answer questions about a document')
    qa_parser.add_argument('source', help='Path to document')
    qa_parser.add_argument('question', help='Question to ask')
    qa_parser.add_argument('--api-key', help='OpenAI API key')
    
    # Summarize command
    summarize_parser = subparsers.add_parser('summarize', help='Generate summary')
    summarize_parser.add_argument('source', help='Path to document')
    summarize_parser.add_argument('--type', choices=['executive', 'bullet', 'tldr'],
                                 default='executive', help='Summary type')
    summarize_parser.add_argument('--api-key', help='OpenAI API key')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Get API key
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key and args.command in ['process', 'qa', 'summarize']:
        print("Error: OpenAI API key required. Set OPENAI_API_KEY environment variable or use --api-key")
        sys.exit(1)
    
    # Initialize DocuMind
    dm = DocuMind(
        api_key=api_key,
        memory_enabled=not getattr(args, 'no_memory', False),
        evaluation_enabled=not getattr(args, 'no_evaluation', False)
    )
    
    # Execute command
    if args.command == 'process':
        result = dm.process_document(
            source=args.source,
            tasks=args.tasks
        )
        
        print(f"\n✓ Document processed: {result['document_id']}")
        print(f"  Source: {result['metadata']['source']}")
        print(f"  Tasks: {', '.join(result['metadata']['tasks'])}")
        
        if result.get('extractions'):
            extractions = result['extractions']
            print(f"\nExtractions:")
            print(f"  Tables: {len(extractions.get('tables', []))}")
            print(f"  Metrics: {len(extractions.get('metrics', []))}")
            print(f"  Dates: {len(extractions.get('dates', []))}")
            print(f"  Tasks: {len(extractions.get('tasks', []))}")
        
        if result.get('summaries'):
            print(f"\nSummaries generated:")
            for summary_type in result['summaries'].keys():
                print(f"  - {summary_type}")
    
    elif args.command == 'qa':
        # Process document first
        result = dm.process_document(
            source=args.source,
            tasks=['qa']
        )
        
        # Answer question
        answer = dm.answer_question(args.question, return_citations=True)
        
        print(f"\nQ: {args.question}")
        print(f"\nA: {answer['answer']}")
        print(f"\nConfidence: {answer['confidence']:.2f}")
        
        if answer.get('citations'):
            print(f"\nCitations:")
            for citation in answer['citations']:
                print(f"  Page {citation['page']}: {citation['text'][:100]}...")
    
    elif args.command == 'summarize':
        result = dm.process_document(
            source=args.source,
            tasks=['summarize']
        )
        
        summary = result['summaries'].get(args.type, 'Summary not available')
        print(f"\n{args.type.upper()} SUMMARY")
        print("=" * 80)
        print(summary)


if __name__ == '__main__':
    main()

