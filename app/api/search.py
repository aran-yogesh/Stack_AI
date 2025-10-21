"""FastAPI endpoints for search operations."""

from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.models import SearchQuery, SearchResponse
from app.repositories.shared import (
    chunk_repository,
    document_repository,
    library_repository,
)
from app.services.chunk_service import ChunkService
from app.services.library_service import LibraryService
from app.services.search_service import SearchService

# Initialize router
router = APIRouter(prefix="/libraries/{library_id}", tags=["search"])

# Initialize services
chunk_service = ChunkService(chunk_repository, document_repository)
library_service = LibraryService(library_repository)
search_service = SearchService(chunk_service)


@router.post("/search", response_model=SearchResponse)
async def search_library(
    library_id: UUID,
    search_query: SearchQuery,
    index_type: str = Query(default="flat", description="Index type: 'flat' or 'ivf'")
):
    """
    Perform k-NN search on a library.
    
    Args:
        library_id: Library ID
        search_query: Search query parameters
        index_type: Type of index to use ("flat" or "ivf")
        
    Returns:
        Search results with similarity scores
        
    Raises:
        HTTPException: If library not found or index not built
    """
    # Check if library exists
    if not await library_service.library_exists(library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    try:
        results = await search_service.search(library_id, search_query, index_type)
        return results
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/index", status_code=status.HTTP_202_ACCEPTED)
async def build_indexes(library_id: UUID):
    """
    Build indexes for a library.
    
    Args:
        library_id: Library ID
        
    Returns:
        Index build statistics
        
    Raises:
        HTTPException: If library not found
    """
    # Check if library exists
    if not await library_service.library_exists(library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    stats = await search_service.build_indexes(library_id)
    return {
        "message": "Index building completed",
        "library_id": library_id,
        "stats": stats
    }


@router.get("/index/stats")
async def get_index_stats(library_id: UUID):
    """
    Get index statistics for a library.
    
    Args:
        library_id: Library ID
        
    Returns:
        Index statistics
        
    Raises:
        HTTPException: If library not found
    """
    # Check if library exists
    if not await library_service.library_exists(library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    stats = await search_service.get_index_stats(library_id)
    return {
        "library_id": library_id,
        "stats": stats
    }


@router.post("/index/rebuild", status_code=status.HTTP_202_ACCEPTED)
async def rebuild_indexes(library_id: UUID):
    """
    Rebuild indexes for a library.
    
    Args:
        library_id: Library ID
        
    Returns:
        Index rebuild statistics
        
    Raises:
        HTTPException: If library not found
    """
    # Check if library exists
    if not await library_service.library_exists(library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    stats = await search_service.rebuild_indexes(library_id)
    return {
        "message": "Index rebuild completed",
        "library_id": library_id,
        "stats": stats
    }


@router.get("/index/available")
async def get_available_indexes(library_id: UUID):
    """
    Get available indexes for a library.
    
    Args:
        library_id: Library ID
        
    Returns:
        List of available index types
        
    Raises:
        HTTPException: If library not found
    """
    # Check if library exists
    if not await library_service.library_exists(library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    available_indexes = search_service.get_available_indexes(library_id)
    return {
        "library_id": library_id,
        "available_indexes": available_indexes
    }
