# Deployment Guide - Stratobet Backend

## Prerequisites
- GitHub account
- Railway account (free): https://railway.app

## Step 1: Prepare Git Repository

```bash
# Initialize git (if not already done)
cd D:\Project\StratoBet\backend
git init

# Create .gitignore
echo "venv/
__pycache__/
*.pyc
.env
.DS_Store
tests/" > .gitignore

# Initial commit
git add .
git commit -m "Initial commit - Stratobet backend with ML model"
```

## Step 2: Push to GitHub

```bash
# Create new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/stratobet-backend.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Railway

1. **Go to Railway.app** → Login with GitHub
2. **New Project** → "Deploy from GitHub repo"
3. **Select** `stratobet-backend` repository
4. **Add PostgreSQL**:
   - Click "+ New"
   - Select "Database"
   - Choose "PostgreSQL"
   - Wait for provisioning

## Step 4: Configure Environment Variables

In Railway dashboard → Variables:

```env
# Database (auto-filled by Railway PostgreSQL)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# API Keys
API_FOOTBALL_KEY=3133433ac52e0dfa04e9c36d9361f4ec
API_FOOTBALL_BASE_URL=https://v3.football.api-sports.io
ODDS_API_KEY=31c30c97b6fe5d0811864f977fa9a7de
ODDS_API_BASE_URL=https://api.the-odds-api.com/v4

# Model
MODEL_PATH=ml-pipeline/models/random_forest_v1.0.0.pkl
MODEL_VERSION=v1.0.0

# CORS (add after deploying frontend)
BACKEND_CORS_ORIGINS=["http://localhost:5173","https://your-frontend.vercel.app"]

# API Config
API_V1_PREFIX=/api/v1
```

## Step 5: Load Database Data

After deployment, you need to populate the database:

**Option A: Using Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Run migration
railway run python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Load data (one-time)
# You'll need to upload data via SQL or API
```

**Option B: Using SQL Dump**
```bash
# Export local database
pg_dump -U postgres stratobet > stratobet_dump.sql

# Import to Railway (connection string from Railway dashboard)
psql "postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway" < stratobet_dump.sql
```

## Step 6: Verify Deployment

Your API will be available at: `https://your-app-name.railway.app`

Test endpoints:
```bash
# Health check
curl https://your-app-name.railway.app/health

# API docs
https://your-app-name.railway.app/docs
```

## Step 7: Update Frontend URL

Once deployed, update CORS in Railway environment variables to include your frontend URL.

## Troubleshooting

**Build fails:**
- Check Railway build logs
- Verify requirements.txt versions
- Ensure ML model is in repo (< 100MB)

**Database connection fails:**
- Verify DATABASE_URL is set
- Check PostgreSQL service is running
- Check firewall rules

**Model not found:**
- Verify model file path
- Check model is committed to Git
- Verify MODEL_PATH environment variable

## Monitoring

Railway provides:
- Real-time logs
- Metrics dashboard
- Automatic SSL
- Custom domains (paid plan)

## Cost

**Free Tier:**
- 500 hours/month
- $5 credit/month
- PostgreSQL included

Should be sufficient for testing and low traffic!
