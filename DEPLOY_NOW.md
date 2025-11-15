# 🚀 Quick Deployment Guide

## Option 1: Railway (Easiest - No CLI Required) ⭐ RECOMMENDED

### Steps:

1. **Go to Railway:**
   - Visit: https://railway.app
   - Sign up/Login with GitHub

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository: `mishraadarsh27/documind11`

3. **Configure:**
   - Railway will auto-detect Python
   - It will use the `railway.json` config file

4. **Set Environment Variable:**
   - Go to "Variables" tab
   - Add: `OPENAI_API_KEY` = `your-api-key-here`

5. **Deploy:**
   - Railway will automatically build and deploy
   - Your app will be live in 2-3 minutes!

**Your app URL will be:** `https://your-app-name.up.railway.app`

---

## Option 2: Render (Also Easy - No CLI Required)

### Steps:

1. **Go to Render:**
   - Visit: https://render.com
   - Sign up/Login with GitHub

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `mishraadarsh27/documind11`

3. **Configure:**
   - **Name:** `documind` (or your choice)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r webapp/requirements.txt && pip install -r requirements.txt`
   - **Start Command:** `cd webapp && gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Set Environment Variable:**
   - Scroll to "Environment Variables"
   - Add: `OPENAI_API_KEY` = `your-api-key-here`

5. **Deploy:**
   - Click "Create Web Service"
   - Render will build and deploy automatically

**Your app URL will be:** `https://documind.onrender.com` (or your custom name)

---

## Option 3: Heroku (Requires CLI Installation)

### Install Heroku CLI First:

**Windows:**
1. Download from: https://devcenter.heroku.com/articles/heroku-cli
2. Run the installer
3. Restart terminal

**Then run:**
```bash
heroku login
heroku create your-documind-app
heroku config:set OPENAI_API_KEY=your-api-key-here
git push heroku main
```

---

## ⚡ Quick Deploy Checklist

- [ ] Choose platform (Railway or Render recommended)
- [ ] Connect GitHub repository
- [ ] Set `OPENAI_API_KEY` environment variable
- [ ] Wait for deployment (2-5 minutes)
- [ ] Test your live URL!

---

## 🎯 After Deployment

Once deployed, you'll have:
- ✅ Live web application
- ✅ File upload interface
- ✅ Document processing
- ✅ Q&A functionality

**Share your live link!** 🎉

---

## 📝 Notes

- **Railway** offers free tier with $5 credit
- **Render** offers free tier (may sleep after inactivity)
- Both platforms auto-deploy on git push
- Both support custom domains

**Recommended: Railway** - Fastest and most reliable free tier!

