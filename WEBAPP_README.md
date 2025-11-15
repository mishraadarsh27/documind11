# DocuMind Web Application

## 🌐 Live Web Interface

DocuMind now includes a **fully functional web application** that you can deploy and access via browser!

## Quick Start

### Option 1: Run Locally

```bash
# Navigate to webapp directory
cd documind/webapp

# Install dependencies
pip install -r requirements.txt
# Also install parent requirements
cd ..
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=your-api-key-here

# Run the app
cd webapp
python app.py
```

Then open: **http://localhost:5000**

### Option 2: Deploy to Heroku

1. **Create Heroku app:**
```bash
heroku create your-documind-app
```

2. **Set environment variable:**
```bash
heroku config:set OPENAI_API_KEY=your-api-key
```

3. **Deploy:**
```bash
git push heroku main
```

Your app will be live at: **https://your-documind-app.herokuapp.com**

### Option 3: Deploy to Railway

1. Go to [Railway.app](https://railway.app)
2. Create new project from GitHub
3. Connect your repository
4. Set environment variable: `OPENAI_API_KEY`
5. Deploy!

### Option 4: Deploy to Render

1. Go to [Render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Set:
   - Build Command: `pip install -r webapp/requirements.txt && pip install -r requirements.txt`
   - Start Command: `cd webapp && gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add environment variable: `OPENAI_API_KEY`
6. Deploy!

## Features

✅ **File Upload** - Upload PDF, TXT, or MD files  
✅ **URL Processing** - Process documents from web URLs  
✅ **Information Extraction** - View tables, metrics, dates, tasks, entities  
✅ **Multiple Summaries** - Executive, Bullet-point, and TL;DR summaries  
✅ **Interactive Q&A** - Ask questions with page-level citations  
✅ **Modern UI** - Beautiful, responsive interface  
✅ **Real-time Processing** - See results as they're generated  

## Web App Structure

```
webapp/
├── app.py              # Flask backend
├── templates/
│   └── index.html      # Main page
├── static/
│   ├── style.css       # Styling
│   └── app.js          # Frontend logic
├── uploads/            # Uploaded files (auto-created)
├── requirements.txt    # Dependencies
├── Procfile            # Heroku config
└── README.md           # Detailed docs
```

## API Endpoints

- `GET /` - Main web interface
- `GET /api/health` - Health check
- `POST /api/process` - Process uploaded file
- `POST /api/process-url` - Process URL
- `POST /api/qa` - Answer questions
- `GET /api/extractions/<id>` - Get extractions

## Screenshots

The web app includes:
- Clean, modern design
- Drag-and-drop file upload
- Real-time processing status
- Interactive results display
- Q&A interface with citations

## Troubleshooting

**API Key Issues:**
- Ensure `OPENAI_API_KEY` is set in environment variables
- Check `/api/health` endpoint

**File Upload Issues:**
- Max file size: 50MB
- Supported formats: PDF, TXT, MD

**Deployment Issues:**
- Ensure all dependencies are in requirements.txt
- Check Python version (3.9+)
- Verify Procfile for Heroku

## Next Steps

1. **Push to GitHub:**
```bash
git add .
git commit -m "Add DocuMind web application"
git push origin main
```

2. **Deploy to your preferred platform** (Heroku, Railway, Render, etc.)

3. **Share your live link!** 🚀

## Support

For issues or questions, check:
- `webapp/README.md` - Detailed webapp documentation
- Main `README.md` - Overall project documentation
- GitHub Issues - Report bugs or request features

---

**Ready to deploy?** Follow the steps above and share your live DocuMind web app! 🎉

