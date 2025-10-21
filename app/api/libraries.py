"""FastAPI endpoints for libraries."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.models import Library, LibraryCreate, LibraryUpdate
from app.repositories.shared import library_repository

# Initialize router
router = APIRouter(prefix="/libraries", tags=["libraries"])

# Services will be injected by main.py
library_service = None


@router.post("/", response_model=Library, status_code=status.HTTP_201_CREATED)
async def create_library(library_data: LibraryCreate):
    """
    Create a new library.
    
    Args:
        library_data: Library creation data
        
    Returns:
        Created library
        
    Raises:
        HTTPException: If library name already exists
    """
    try:
        library = await library_service.create_library(library_data)
        return library
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("/", response_model=List[Library])
async def get_all_libraries():
    """
    Get all libraries.
    
    Returns:
        List of all libraries
    """
    libraries = await library_service.get_all_libraries()
    return libraries


@router.get("/{library_id}", response_model=Library)
async def get_library(library_id: UUID):
    """
    Get a library by ID.
    
    Args:
        library_id: Library ID
        
    Returns:
        Library data
        
    Raises:
        HTTPException: If library not found
    """
    library = await library_service.get_library(library_id)
    if not library:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    return library


@router.put("/{library_id}", response_model=Library)
async def update_library(library_id: UUID, library_data: LibraryUpdate):
    """
    Update a library.
    
    Args:
        library_id: Library ID
        library_data: Library update data
        
    Returns:
        Updated library
        
    Raises:
        HTTPException: If library not found or name conflict
    """
    try:
        library = await library_service.update_library(library_id, library_data)
        if not library:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Library with ID {library_id} not found"
            )
        return library
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{library_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_library(library_id: UUID):
    """
    Delete a library.
    
    Args:
        library_id: Library ID
        
    Raises:
        HTTPException: If library not found
    """
    deleted = await library_service.delete_library(library_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None
    )
