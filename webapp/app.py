"""
DocuMind Web Application - Flask Backend
"""

import os
import uuid
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
from pathlib import Path
from loguru import logger

# Import DocuMind
import sys
# Add parent directory to path to import documind
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from documind import DocuMind

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'md', 'text'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)

# Initialize DocuMind
documind = None

def init_documind():
    """Initialize DocuMind with FREE models (no API key required!)"""
    global documind
    # Use FREE models by default - no API key needed!
    documind = DocuMind(
        use_free_models=True,  # Use FREE Hugging Face models
        ocr_enabled=True,
        memory_enabled=True,
        evaluation_enabled=True
    )
    logger.info("DocuMind initialized with FREE models - No API key required!")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'documind_initialized': documind is not None,
        'using_free_models': True,
        'message': 'Using FREE Hugging Face models - No API key required!'
    })

@app.route('/api/process', methods=['POST'])
def process_document():
    """Process uploaded document"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use PDF or TXT files.'}), 400
        
        # Get tasks from request
        tasks = request.form.get('tasks', 'extract,summarize').split(',')
        
        # Save file
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file_ext = filename.rsplit('.', 1)[1].lower()
        saved_filename = f"{file_id}.{file_ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        file.save(filepath)
        
        logger.info(f"Processing file: {filename} (ID: {file_id})")
        
        # Process document
        if not documind:
            init_documind()
        
        result = documind.process_document(
            source=filepath,
            tasks=tasks,
            document_id=file_id,
            store_in_memory=True
        )
        
        # Prepare response
        response_data = {
            'document_id': result['document_id'],
            'metadata': result['document']['metadata'],
            'extractions': {
                'tables_count': len(result.get('extractions', {}).get('tables', [])),
                'metrics_count': len(result.get('extractions', {}).get('metrics', [])),
                'dates_count': len(result.get('extractions', {}).get('dates', [])),
                'tasks_count': len(result.get('extractions', {}).get('tasks', [])),
                'entities_count': len(result.get('extractions', {}).get('entities', {}).get('all', [])) if isinstance(result.get('extractions', {}).get('entities'), dict) else 0
            },
            'summaries': result.get('summaries', {}),
            'has_qa': result.get('qa') is not None
        }
        
        # Store full result in session (in production, use Redis or database)
        result_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_result.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process-url', methods=['POST'])
def process_url():
    """Process document from URL"""
    try:
        data = request.get_json()
        url = data.get('url')
        tasks = data.get('tasks', ['extract', 'summarize'])
        
        if not url:
            return jsonify({'error': 'URL not provided'}), 400
        
        if not documind:
            init_documind()
        
        result = documind.process_document(
            source=url,
            tasks=tasks,
            store_in_memory=True
        )
        
        response_data = {
            'document_id': result['document_id'],
            'metadata': result['document']['metadata'],
            'extractions': {
                'tables_count': len(result.get('extractions', {}).get('tables', [])),
                'metrics_count': len(result.get('extractions', {}).get('metrics', [])),
                'dates_count': len(result.get('extractions', {}).get('dates', [])),
                'tasks_count': len(result.get('extractions', {}).get('tasks', [])),
                'entities_count': len(result.get('extractions', {}).get('entities', {}).get('all', [])) if isinstance(result.get('extractions', {}).get('entities'), dict) else 0
            },
            'summaries': result.get('summaries', {}),
            'has_qa': result.get('qa') is not None
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error processing URL: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/qa', methods=['POST'])
def answer_question():
    """Answer question about document"""
    try:
        data = request.get_json()
        document_id = data.get('document_id')
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'Question not provided'}), 400
        
        if not documind:
            init_documind()
        
        # Load document result if needed
        result_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{document_id}_result.json")
        if os.path.exists(result_file):
            with open(result_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
            # Re-setup Q&A if needed
            if not documind.current_document:
                documind.current_document = result['document']
                documind.qa.setup_document(result['document'])
        
        answer = documind.answer_question(question, return_citations=True)
        
        return jsonify(answer)
        
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/extractions/<document_id>', methods=['GET'])
def get_extractions(document_id):
    """Get detailed extractions for a document"""
    try:
        result_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{document_id}_result.json")
        if not os.path.exists(result_file):
            return jsonify({'error': 'Document not found'}), 404
        
        with open(result_file, 'r', encoding='utf-8') as f:
            result = json.load(f)
        
        return jsonify(result.get('extractions', {}))
        
    except Exception as e:
        logger.error(f"Error getting extractions: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_documind()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

# For Gunicorn
if __name__ != '__main__':
    init_documind()

