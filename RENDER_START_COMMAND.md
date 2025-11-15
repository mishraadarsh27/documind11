# Render Start Command

## ✅ Correct Start Command for Render:

```
cd webapp && gunicorn app:app --bind 0.0.0.0:$PORT
```

## 📋 Complete Render Configuration:

### Build Command:
```
pip install -r webapp/requirements.txt && pip install -r requirements.txt && python -m spacy download en_core_web_sm
```

### Start Command:
```
cd webapp && gunicorn app:app --bind 0.0.0.0:$PORT
```

### Environment Variables:
**None required!** DocuMind uses FREE models - no API key needed! 🎉

## 🚀 Quick Deploy Steps:

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repo: `mishraadarsh27/documind11`
4. Set:
   - **Build Command:** `pip install -r webapp/requirements.txt && pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command:** `cd webapp && gunicorn app:app --bind 0.0.0.0:$PORT`
5. Click "Create Web Service"
6. Wait for deployment (5-10 minutes first time - models download)
7. Done! Your app is live!

## ⚠️ Important Notes:

- **First deployment takes longer** (~10-15 minutes) because models download
- **No environment variables needed** - completely FREE!
- **Port is automatic** - Render provides `$PORT` variable
- **Gunicorn is required** - already in `webapp/requirements.txt`

## 🔍 Troubleshooting:

**If deployment fails:**
- Check build logs for errors
- Ensure all dependencies are in requirements.txt
- Verify Python version (3.9+)

**If app doesn't start:**
- Check start command is exactly: `cd webapp && gunicorn app:app --bind 0.0.0.0:$PORT`
- Verify gunicorn is in requirements.txt
- Check logs for specific errors

---

**That's it!** Copy and paste the start command above into Render! 🚀

