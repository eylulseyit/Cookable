from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.database import engine
from app.models import database_models

# Create database tables on startup
database_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Recipe Recommendation API",
    description="AI-powered recipe recommendation based on available ingredients",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Recipe Recommendation API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "recipe-recommendation-api"} 