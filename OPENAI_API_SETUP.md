# OpenAI API Key Setup Guide

## 🔑 How to Get Your OpenAI API Key

### Step-by-Step Instructions:

1. **Visit OpenAI Platform:**
   - Go to: https://platform.openai.com
   - Sign up (if new) or Log in

2. **Navigate to API Keys:**
   - Click on your profile (top right)
   - Select "API Keys"
   - Or go directly: https://platform.openai.com/api-keys

3. **Create New Key:**
   - Click "Create new secret key"
   - Give it a name: `DocuMind` or `My Project`
   - Click "Create secret key"

4. **Copy Your Key:**
   - ⚠️ **IMPORTANT:** Copy the key immediately!
   - You won't be able to see it again
   - It looks like: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

5. **Store Securely:**
   - Never share your API key publicly
   - Don't commit it to GitHub
   - Use environment variables

## 💰 Pricing Information

### Free Tier:
- ✅ **$5 free credit** for new accounts
- ✅ Valid for 3 months
- ✅ Perfect for testing and development

### After Free Tier:
- Pay-as-you-go pricing
- Only pay for what you use
- No monthly fees

### Cost Estimates:

**GPT-4 Turbo (Default):**
- ~$0.01-0.03 per document (summaries)
- ~$0.001 per question (Q&A)

**GPT-3.5 Turbo (Cheaper Option):**
- ~$0.001-0.003 per document
- ~$0.0001 per question
- **10x cheaper than GPT-4!**

### Example Monthly Costs:

| Usage | GPT-4 Cost | GPT-3.5 Cost |
|-------|-----------|--------------|
| 10 documents/month | ~$0.30 | ~$0.03 |
| 100 documents/month | ~$3.00 | ~$0.30 |
| 1000 documents/month | ~$30.00 | ~$3.00 |

## 🎯 Using Your API Key

### For Local Development:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-proj-your-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=sk-proj-your-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-proj-your-key-here"
```

### For Deployment (Railway/Render):

1. Go to your deployment platform
2. Find "Environment Variables" or "Config"
3. Add: `OPENAI_API_KEY` = `your-key-here`
4. Save and redeploy

## 💡 Cost-Saving Tips

### 1. Use GPT-3.5 Instead of GPT-4

Edit `documind/documind/agents/analyzer.py`:
```python
# Change line ~20 from:
model: str = "gpt-4-turbo-preview"
# To:
model: str = "gpt-3.5-turbo"  # Much cheaper!
```

### 2. Monitor Your Usage

- Visit: https://platform.openai.com/usage
- Set up usage limits
- Get alerts when approaching limits

### 3. Set Usage Limits

1. Go to: https://platform.openai.com/account/billing/limits
2. Set hard limits (e.g., $10/month)
3. Get notified before exceeding

### 4. Use Free Tier Wisely

- Start with free $5 credit
- Test thoroughly before scaling
- Switch to GPT-3.5 for production

## 🔒 Security Best Practices

1. **Never commit API keys to GitHub**
   - Use `.env` file (already in `.gitignore`)
   - Use environment variables

2. **Rotate keys regularly**
   - Generate new keys periodically
   - Revoke old unused keys

3. **Use different keys for different projects**
   - Easier to track usage
   - Better security isolation

## 📊 Check Your Usage

- **Dashboard:** https://platform.openai.com/usage
- **Billing:** https://platform.openai.com/account/billing
- **API Keys:** https://platform.openai.com/api-keys

## ❓ FAQ

**Q: Is OpenAI API free?**
A: New accounts get $5 free credit. After that, it's pay-as-you-go.

**Q: How much does it cost?**
A: Depends on usage. GPT-3.5 is ~$0.001-0.003 per document.

**Q: Can I use it without credit card?**
A: Yes, for the free tier. But you'll need to add payment method after free credit expires.

**Q: What if I exceed my budget?**
A: Set usage limits in OpenAI dashboard to prevent unexpected charges.

**Q: Are there free alternatives?**
A: Yes! See `FREE_ALTERNATIVES.md` for options using Hugging Face or local models.

## 🚀 Quick Start

1. Get API key from https://platform.openai.com/api-keys
2. Set environment variable: `OPENAI_API_KEY=your-key`
3. Start using DocuMind!

**That's it!** You're ready to go! 🎉

