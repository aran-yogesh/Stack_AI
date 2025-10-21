"""FastAPI endpoints for documents."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.models import Document, DocumentCreate, DocumentUpdate
from app.repositories.shared import document_repository, library_repository

# Initialize router
router = APIRouter(prefix="/libraries/{library_id}/documents", tags=["documents"])

# Services will be injected by main.py
document_service = None
library_service = None

# Dependency injection will be set up in main.py to avoid circular imports


@router.post("/", response_model=Document, status_code=status.HTTP_201_CREATED)
async def create_document(library_id: UUID, document_data: DocumentCreate):
    """
    Create a new document in a library.
    
    Args:
        library_id: Parent library ID
        document_data: Document creation data
        
    Returns:
        Created document
        
    Raises:
        HTTPException: If library not found or document title already exists
    """
    try:
        document = await document_service.create_document(library_id, document_data)
        return document
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )


@router.get("/", response_model=List[Document])
async def get_documents_in_library(library_id: UUID):
    """
    Get all documents in a library.
    
    Args:
        library_id: Library ID
        
    Returns:
        List of documents in the library
        
    Raises:
        HTTPException: If library not found
    """
    # Check if library exists
    if not await library_service.library_exists(library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    documents = await document_service.get_documents_by_library(library_id)
    return documents


@router.get("/{document_id}", response_model=Document)
async def get_document(library_id: UUID, document_id: UUID):
    """
    Get a document by ID.
    
    Args:
        library_id: Library ID
        document_id: Document ID
        
    Returns:
        Document data
        
    Raises:
        HTTPException: If library or document not found
    """
    # Check if library exists
    if not await library_service.library_exists(library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    document = await document_service.get_document(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found"
        )
    
    # Verify document belongs to library
    if document.library_id != library_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found in library {library_id}"
        )
    
    return document


@router.put("/{document_id}", response_model=Document)
async def update_document(library_id: UUID, document_id: UUID, document_data: DocumentUpdate):
    """
    Update a document.
    
    Args:
        library_id: Library ID
        document_id: Document ID
        document_data: Document update data
        
    Returns:
        Updated document
        
    Raises:
        HTTPException: If library or document not found, or title conflict
    """
    # Check if library exists
    if not await library_service.library_exists(library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    try:
        document = await document_service.update_document(document_id, document_data)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found"
            )
        
        # Verify document belongs to library
        if document.library_id != library_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found in library {library_id}"
            )
        
        return document
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(library_id: UUID, document_id: UUID):
    """
    Delete a document.
    
    Args:
        library_id: Library ID
        document_id: Document ID
        
    Raises:
        HTTPException: If library or document not found
    """
    # Check if library exists
    if not await library_service.library_exists(library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    # Check if document exists and belongs to library
    document = await document_service.get_document(document_id)
    if not document or document.library_id != library_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found in library {library_id}"
        )
    
    deleted = await document_service.delete_document(document_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} not found"
        )
    
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None
    )
