"""Main FastAPI application."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import chunks, csv_export, documents, libraries, search
from app.config import settings
from app.services.service_manager import service_manager

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A REST API for indexing and querying documents within a Vector Database",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up service dependencies in API modules
libraries.document_service = service_manager.document_service
libraries.library_service = service_manager.library_service

documents.document_service = service_manager.document_service
documents.library_service = service_manager.library_service

chunks.chunk_service = service_manager.chunk_service
chunks.document_service = service_manager.document_service
chunks.library_service = service_manager.library_service

search.chunk_service = service_manager.chunk_service
search.library_service = service_manager.library_service
search.search_service = service_manager.search_service

csv_export.chunk_service = service_manager.chunk_service
csv_export.document_service = service_manager.document_service
csv_export.library_service = service_manager.library_service

# Include routers
app.include_router(libraries.router)
app.include_router(documents.router)
app.include_router(chunks.router)
app.include_router(search.router)
app.include_router(csv_export.router)


@app.get("/", response_class=JSONResponse)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Vector Database API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "libraries": "/libraries",
            "documents": "/libraries/{library_id}/documents",
            "chunks": "/libraries/{library_id}/documents/{document_id}/chunks",
            "search": "/libraries/{library_id}/search"
        }
    }


@app.get("/health", response_class=JSONResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "Vector Database API is running"
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
