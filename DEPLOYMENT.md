# DocuMind Deployment Guide

## Deployment Options

### 1. Kaggle Notebook

DocuMind is designed to run in Kaggle notebooks for demonstration purposes.

**Steps:**
1. Upload the `documind` folder to Kaggle
2. Upload sample documents
3. Open `notebooks/documind_demo.ipynb`
4. Set your OpenAI API key
5. Run all cells

**Requirements:**
- Kaggle account
- OpenAI API key
- Sample documents (PDF, text, or URLs)

### 2. Local Installation

**Steps:**
1. Clone repository: `git clone <repo-url>`
2. Navigate to directory: `cd documind`
3. Create virtual environment: `python -m venv venv`
4. Activate: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install: `pip install -r requirements.txt`
6. Install spaCy model: `python -m spacy download en_core_web_sm`
7. Set environment variable: `export OPENAI_API_KEY=your-key`
8. Run: `python -m documind.cli process document.pdf`

### 3. GitHub Repository

**Repository Structure:**
```
documind/
├── documind/          # Source code
├── notebooks/         # Kaggle notebook
├── examples/          # Example scripts
├── tests/             # Unit tests
├── README.md          # Main documentation
├── requirements.txt   # Dependencies
└── setup.py           # Installation script
```

**GitHub Setup:**
1. Create new repository
2. Push code: `git push origin main`
3. Add README badges
4. Set up GitHub Actions for testing (optional)

### 4. Docker Deployment (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . .

CMD ["python", "-m", "documind.cli"]
```

Build and run:
```bash
docker build -t documind .
docker run -e OPENAI_API_KEY=your-key documind process document.pdf
```

## Environment Variables

Required:
- `OPENAI_API_KEY`: Your OpenAI API key

Optional:
- `MEMORY_STORAGE_PATH`: Path for memory storage (default: `./memory_bank`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `TESSERACT_CMD`: Path to tesseract executable

## Production Considerations

1. **API Key Security**: Never commit API keys. Use environment variables or secrets management.

2. **Rate Limiting**: Implement rate limiting for API calls to avoid exceeding OpenAI quotas.

3. **Error Handling**: Add comprehensive error handling for production use.

4. **Logging**: Configure proper logging for production monitoring.

5. **Memory Management**: For large-scale deployments, consider using a database instead of JSON files for memory storage.

6. **Scaling**: For high-volume usage, consider:
   - Using a task queue (Celery, RQ)
   - Implementing caching
   - Using cloud storage for documents
   - Load balancing for multiple instances

## Monitoring

Monitor:
- API usage and costs
- Processing times
- Error rates
- Memory usage
- Storage usage

## Support

For deployment issues, open an issue on GitHub.

