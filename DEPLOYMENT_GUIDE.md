# DocuMind Deployment Guide

## 🚀 Quick Deployment Options

### 1. Heroku (Recommended for Quick Start)

**Steps:**

1. **Install Heroku CLI** (if not installed):
   ```bash
   # Visit https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku app:**
   ```bash
   cd documind
   heroku create your-documind-app
   ```

4. **Set environment variable:**
   ```bash
   heroku config:set OPENAI_API_KEY=your-openai-api-key-here
   ```

5. **Deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

6. **Your app is live at:**
   ```
   https://your-documind-app.herokuapp.com
   ```

**Note:** For the webapp, you may need to create a separate Heroku app in the `webapp` directory with its own Procfile.

### 2. Railway

**Steps:**

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Connect your GitHub repository
4. Add environment variable: `OPENAI_API_KEY`
5. Set start command: `cd webapp && gunicorn app:app --bind 0.0.0.0:$PORT`
6. Deploy!

### 3. Render

**Steps:**

1. Go to [render.com](https://render.com)
2. Create new "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command:** `pip install -r webapp/requirements.txt && pip install -r requirements.txt`
   - **Start Command:** `cd webapp && gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add environment variable: `OPENAI_API_KEY`
6. Deploy!

### 4. Local Development

**Steps:**

```bash
# 1. Clone/navigate to project
cd documind

# 2. Install dependencies
pip install -r requirements.txt
pip install -r webapp/requirements.txt

# 3. Set environment variable
export OPENAI_API_KEY=your-api-key-here

# 4. Run webapp
cd webapp
python app.py

# 5. Open browser
# http://localhost:5000
```

## 📋 Pre-Deployment Checklist

- [ ] OpenAI API key obtained
- [ ] All dependencies installed
- [ ] Environment variables set
- [ ] Tested locally
- [ ] Git repository initialized
- [ ] `.gitignore` configured (uploads/, .env, etc.)

## 🔧 Configuration

### Required Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)

### Optional Environment Variables

- `PORT` - Port to run on (default: 5000)
- `FLASK_ENV` - Set to `development` for debug mode
- `MEMORY_STORAGE_PATH` - Path for memory storage

## 📁 Project Structure for Deployment

```
documind/
├── documind/          # Core package
├── webapp/           # Web application
│   ├── app.py        # Flask app
│   ├── templates/    # HTML
│   ├── static/       # CSS/JS
│   ├── Procfile      # Heroku config
│   └── requirements.txt
├── requirements.txt  # Main dependencies
└── README.md
```

## 🌐 After Deployment

Once deployed, your web application will be accessible at:
- **Heroku:** `https://your-app-name.herokuapp.com`
- **Railway:** `https://your-app-name.up.railway.app`
- **Render:** `https://your-app-name.onrender.com`

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Working:**
   - Verify environment variable is set correctly
   - Check `/api/health` endpoint

2. **Import Errors:**
   - Ensure all dependencies are in requirements.txt
   - Check Python version (3.9+)

3. **File Upload Issues:**
   - Check file size limits (50MB max)
   - Verify file formats (PDF, TXT, MD)

4. **Deployment Fails:**
   - Check build logs
   - Verify Procfile format
   - Ensure all dependencies are listed

## 📝 GitHub Setup

To push to GitHub:

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial DocuMind deployment"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/documind.git

# Push
git push -u origin main
```

## 🔗 Share Your Deployment

Once deployed, share your link! The web app includes:
- ✅ File upload interface
- ✅ URL processing
- ✅ Real-time results
- ✅ Interactive Q&A
- ✅ Beautiful UI

## 📚 Additional Resources

- [WEBAPP_README.md](WEBAPP_README.md) - Detailed webapp docs
- [README.md](README.md) - Main project documentation
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference

---

**Ready to deploy?** Follow the steps above and share your live DocuMind web app! 🎉

