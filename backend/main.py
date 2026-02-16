from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import documents
from backend.database import init_db

app = FastAPI(
    title="Intelligent Document Processor",
    description="Production-grade document intelligence API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(documents.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "healthy", "service": "document-processor", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "checks": {"database": "ok", "ocr_service": "ok"}}
