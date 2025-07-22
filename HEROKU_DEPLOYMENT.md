# Heroku Deployment Guide for Mood Match

## Prerequisites
1. Install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli
2. Create a Heroku account at: https://heroku.com

## Deployment Steps

### 1. Login to Heroku
```bash
heroku login
```

### 2. Create a new Heroku app (or use existing)
```bash
# Create new app
heroku create your-app-name

# OR if you already have an app
heroku git:remote -a mood-match-ai-e84a7a0d8c6f
```

### 3. Set environment variables (if needed)
```bash
heroku config:set FLASK_ENV=production
heroku config:set PYTHONPATH=backend
```

### 4. Deploy to Heroku
```bash
git push heroku main
```

### 5. Scale the web dyno
```bash
heroku ps:scale web=1
```

### 6. View logs
```bash
heroku logs --tail
```

### 7. Open your app
```bash
heroku open
```

## Important Files for Heroku:

✅ **Procfile** - Tells Heroku how to run your app
```
web: gunicorn wsgi:app
```

✅ **requirements.txt** - Python dependencies
- Updated with all ML dependencies including torch, transformers, spacy

✅ **runtime.txt** - Python version
```
python-3.11.0
```

✅ **wsgi.py** - WSGI entry point
- Properly configured to run the Flask app

## Your app structure is ready for deployment!

## Troubleshooting:

1. **If build fails due to memory issues:**
   - Heroku has limited build memory for free dynos
   - Consider using smaller PyTorch CPU version

2. **If spaCy model fails to load:**
   - The en_core_web_sm model is included in requirements.txt

3. **If the app doesn't start:**
   - Check logs with `heroku logs --tail`
   - Ensure all file paths are relative to the project root

## After successful deployment:
Your backend will be available at: https://your-app-name.herokuapp.com
Update the frontend fetch URL to point to your new Heroku app URL.
