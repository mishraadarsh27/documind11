# DocuMind Web Application

Web interface for DocuMind AI Document Intelligence Agent.

## Features

- 📄 Upload PDF, TXT, or MD files
- 🌐 Process documents from URLs
- 📊 View extracted information (tables, metrics, dates, tasks, entities)
- 📝 Generate multiple summary types (Executive, Bullet, TL;DR)
- ❓ Interactive Q&A with citations
- 🎨 Modern, responsive UI

## Quick Start

### Local Development

1. **Install dependencies:**
```bash
cd webapp
pip install -r requirements.txt
# Also install parent requirements
cd ..
pip install -r requirements.txt
```

2. **Set environment variable:**
```bash
export OPENAI_API_KEY=your-api-key-here
```

3. **Run the application:**
```bash
cd webapp
python app.py
```

4. **Open in browser:**
```
http://localhost:5000
```

## Deployment

### Heroku

1. **Create Heroku app:**
```bash
heroku create documind-app
```

2. **Set environment variable:**
```bash
heroku config:set OPENAI_API_KEY=your-api-key
```

3. **Deploy:**
```bash
git push heroku main
```

### Railway

1. Connect your GitHub repository
2. Set `OPENAI_API_KEY` in environment variables
3. Set start command: `gunicorn app:app`
4. Deploy

### Render

1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt && cd .. && pip install -r requirements.txt`
4. Set start command: `cd webapp && gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add environment variable: `OPENAI_API_KEY`

### Vercel/Netlify (Frontend Only)

For frontend-only deployment, you'll need to:
1. Build static files
2. Update API endpoints to point to your backend
3. Deploy static files

## Configuration

### Environment Variables

- `OPENAI_API_KEY` (required): Your OpenAI API key
- `PORT` (optional): Port to run on (default: 5000)
- `FLASK_ENV` (optional): Set to `development` for debug mode

### File Upload Limits

- Maximum file size: 50MB
- Allowed formats: PDF, TXT, MD

## Project Structure

```
webapp/
├── app.py              # Flask application
├── templates/          # HTML templates
│   └── index.html
├── static/             # Static files
│   ├── style.css
│   └── app.js
├── uploads/            # Uploaded files (gitignored)
├── requirements.txt    # Python dependencies
├── Procfile            # Heroku deployment config
└── README.md
```

## API Endpoints

- `GET /` - Main page
- `GET /api/health` - Health check
- `POST /api/process` - Process uploaded file
- `POST /api/process-url` - Process document from URL
- `POST /api/qa` - Answer question about document
- `GET /api/extractions/<document_id>` - Get detailed extractions

## Troubleshooting

### API Key Not Set
- Ensure `OPENAI_API_KEY` environment variable is set
- Check the health endpoint: `/api/health`

### File Upload Fails
- Check file size (max 50MB)
- Verify file format (PDF, TXT, MD)
- Check server logs for errors

### Q&A Not Working
- Ensure "Enable Q&A" task is selected
- Check that document was processed with Q&A enabled
- Verify OpenAI API key is valid

## License

MIT License - See parent directory LICENSE file

