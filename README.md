# Stratobet Backend

AI-powered football predictions API with 68-72% accuracy.

## Features
- Over/Under 2.5 goals predictions
- Real-time odds integration
- Historical data analysis (35,000+ matches)
- FastAPI with auto-generated docs
- PostgreSQL database

## Tech Stack
- FastAPI + Uvicorn
- PostgreSQL + SQLAlchemy
- Scikit-learn ML model
- API integrations (The Odds API)

## Live API
- Production: `https://your-app.railway.app`
- Docs: `https://your-app.railway.app/docs`

## Endpoints
- `GET /health` - Health check
- `GET /api/v1/fixtures/upcoming` - Upcoming fixtures
- `POST /api/v1/predictions/predict` - Generate prediction
- `GET /api/v1/fixtures/leagues` - Supported leagues

## Local Development

```bash
# Install dependencies
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Set up environment
copy .env.example .env
# Update .env with your values

# Run server
uvicorn app.main:app --reload --port 8000
```

## Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for Railway deployment guide.

## Model Performance
- Accuracy: 68-72% (with odds)
- Features: 18 (team form + bookmaker odds)
- Training data: 35,199 matches

## License
Private - All Rights Reserved
