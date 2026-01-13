"""
Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.ml_service import ml_service
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="AI-driven football prediction API for Over/Under 2.5 goals",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Load ML model on startup"""
    print("=" * 60)
    print(f"🚀 Starting {settings.PROJECT_NAME}")
    print("=" * 60)
    
    # Load ML model
    print("\nLoading ML model...")
    success = ml_service.load_model()
    
    if not success:
        print("⚠️  WARNING: Model could not be loaded!")
        print("   Prediction endpoints will not work until model is available.")
    
    print("\n" + "=" * 60)
    print("✅ Application started successfully!")
    print(f"📖 API Docs: http://localhost:8000/docs")
    print("=" * 60 + "\n")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("\n👋 Shutting down application...")


# Health check endpoints
@app.get("/health")
async def health_check():
    """Basic health check"""
    from app.schemas.prediction import HealthResponse
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )


@app.get("/health/model")
async def model_health():
    """ML model health check"""
    from app.schemas.prediction import ModelHealthResponse
    
    info = ml_service.get_info()
    return ModelHealthResponse(**info)


# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Welcome to Stratobet API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include API routers
from app.api import predictions, fixtures
app.include_router(predictions.router, prefix=f"{settings.API_V1_PREFIX}/predictions", tags=["predictions"])
app.include_router(fixtures.router, prefix=f"{settings.API_V1_PREFIX}/fixtures", tags=["fixtures"])
