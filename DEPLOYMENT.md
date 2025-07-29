# 🚀 Deployment Guide - Stock Market Analysis Dashboard

This guide covers multiple deployment options for your stock market analysis dashboard.

## 📋 Prerequisites

- Git repository with your code
- GitHub account (for most platforms)
- Basic command line knowledge

## 🌐 Deployment Options

### 1. Heroku (Recommended for beginners)

**Steps:**
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login to Heroku:
   ```bash
   heroku login
   ```
3. Create a new Heroku app:
   ```bash
   heroku create your-stock-dashboard-name
   ```
4. Deploy:
   ```bash
   git add .
   git commit -m "Deploy stock market dashboard"
   git push heroku main
   ```

**Files needed:** ✅ Already created
- `Procfile`
- `requirements.txt` (with gunicorn)
- `runtime.txt`

**Cost:** Free tier available (with limitations)

### 2. Railway (Modern & Fast)

**Steps:**
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys

**Files needed:** ✅ Already created
- `railway.toml`
- `requirements.txt`

**Cost:** $5/month after free credits

### 3. Render (Great free tier)

**Steps:**
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect your GitHub repository
5. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT dashboard:server`

**Files needed:** ✅ Already created
- `render.yaml` (optional, for advanced config)
- `requirements.txt`

**Cost:** Free tier available

### 4. Docker Deployment

**For any cloud provider supporting Docker:**

1. Build the image:
   ```bash
   docker build -t stock-dashboard .
   ```

2. Run locally to test:
   ```bash
   docker run -p 8080:8080 stock-dashboard
   ```

3. Deploy to your preferred platform:
   - Google Cloud Run
   - AWS ECS
   - Azure Container Instances
   - DigitalOcean App Platform

**Files needed:** ✅ Already created
- `Dockerfile`
- `.dockerignore`

## 🔧 Environment Variables

For production deployment, you may want to set:

```bash
PORT=8080                    # Port for the application
DEBUG=False                  # Disable debug mode
HOST=0.0.0.0                # Allow external connections
PYTHONUNBUFFERED=1          # Better logging
```

## 📊 Performance Optimization

**For production deployments:**

1. **Caching**: The app fetches stock data on startup. Consider implementing Redis caching for better performance.

2. **Workers**: For high traffic, increase gunicorn workers:
   ```bash
   gunicorn --workers 4 --threads 2 dashboard:server
   ```

3. **Memory**: Stock data analysis is memory-intensive. Ensure at least 512MB RAM.

## 🚨 Important Notes

1. **API Limits**: Yahoo Finance has rate limits. For high-traffic deployments, consider upgrading to a paid financial data API.

2. **Cold Starts**: Free tiers may have cold start delays. First load might take 30-60 seconds.

3. **Data Refresh**: Stock data is fetched on app startup. Restart the app daily for fresh data.

## 🔍 Troubleshooting

**Common Issues:**

1. **Memory errors**: Reduce the number of stocks or time period
2. **Timeout errors**: Increase timeout in gunicorn config
3. **Import errors**: Ensure all dependencies are in requirements.txt

**Logs:**
- Heroku: `heroku logs --tail`
- Railway: Check dashboard logs
- Render: View logs in dashboard

## 🎯 Quick Deploy Commands

**Heroku:**
```bash
git add . && git commit -m "Deploy" && git push heroku main
```

**Railway:**
```bash
git add . && git commit -m "Deploy" && git push origin main
```

**Docker:**
```bash
docker build -t stock-dashboard . && docker run -p 8080:8080 stock-dashboard
```

## 📈 Post-Deployment

After deployment, your dashboard will be available at:
- Heroku: `https://your-app-name.herokuapp.com`
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`

**Features available:**
- Interactive time series analysis
- Real-time correlation matrices
- Portfolio optimization metrics
- Risk-adjusted return calculations
- Advanced financial analytics

## 🔗 Custom Domain

Most platforms support custom domains:
1. Purchase a domain
2. Add CNAME record pointing to your app
3. Configure in platform dashboard

---

**Need help?** Check the platform-specific documentation or create an issue in the repository.