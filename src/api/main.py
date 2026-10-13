from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.database.connection import SessionLocal, test_connection
from src.api import transactions, products, customers, analytics

# Initialize FastAPI app
app = FastAPI(
    title="Retail Analytics Platform API",
    description="REST API for online retail transaction analytics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test database connection on startup
@app.on_event("startup")
async def startup():
    """Test database connection on startup"""
    if test_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Check if API is running"""
    return {
        "status": "healthy",
        "message": "Retail Analytics API is running",
        "version": "1.0.0"
    }

# Include routers from other modules
app.include_router(
    transactions.router,
    prefix="/api/v1/transactions",
    tags=["Transactions"]
)

app.include_router(
    products.router,
    prefix="/api/v1/products",
    tags=["Products"]
)

app.include_router(
    customers.router,
    prefix="/api/v1/customers",
    tags=["Customers"]
)

app.include_router(
    analytics.router,
    prefix="/api/v1/analytics",
    tags=["Analytics"]
)

# Root endpoint
@app.get("/", tags=["Info"])
async def root():
    """Welcome to Retail Analytics API"""
    return {
        "message": "Welcome to Retail Analytics Platform API",
        "docs": "Visit /docs for interactive API documentation",
        "endpoints": {
            "transactions": "/api/v1/transactions",
            "products": "/api/v1/products",
            "customers": "/api/v1/customers",
            "analytics": "/api/v1/analytics"
        }
    }

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()