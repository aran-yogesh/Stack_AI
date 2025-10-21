"""FastAPI endpoints for chunks."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.models import Chunk, ChunkCreate, ChunkUpdate
from app.repositories.shared import (
    chunk_repository,
    document_repository,
    library_repository,
)

# Initialize router
router = APIRouter(prefix="/libraries/{library_id}/documents/{document_id}/chunks", tags=["chunks"])

# Services will be injected by main.py
chunk_service = None
document_service = None
library_service = None


@router.post("/", response_model=Chunk, status_code=status.HTTP_201_CREATED)
async def create_chunk(library_id: UUID, document_id: UUID, chunk_data: ChunkCreate):
    """
    Create a new chunk in a document.
    
    Args:
        library_id: Parent library ID
        document_id: Parent document ID
        chunk_data: Chunk creation data
        
    Returns:
        Created chunk with embedding
        
    Raises:
        HTTPException: If library or document not found
    """
    # Check if library exists
    if not await library_service.library_exists(library_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Library with ID {library_id} not found"
        )
    
    try:
        chunk = await chunk_service.create_chunk(document_id, chunk_data)
        
        # Verify document belongs to library
        document = await document_service.get_document(document_id)
        if not document or document.library_id != library_id:
            # Clean up the created chunk
            await chunk_service.delete_chunk(chunk.id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document with ID {document_id} not found in library {library_id}"
            )
        
        return chunk
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/", response_model=List[Chunk])
async def get_chunks_in_document(library_id: UUID, document_id: UUID):
    """
    Get all chunks in a document.
    
    Args:
        library_id: Library ID
        document_id: Document ID
        
    Returns:
        List of chunks in the document
        
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
    
    chunks = await chunk_service.get_chunks_by_document(document_id)
    return chunks


@router.get("/{chunk_id}", response_model=Chunk)
async def get_chunk(library_id: UUID, document_id: UUID, chunk_id: UUID):
    """
    Get a chunk by ID.
    
    Args:
        library_id: Library ID
        document_id: Document ID
        chunk_id: Chunk ID
        
    Returns:
        Chunk data
        
    Raises:
        HTTPException: If library, document, or chunk not found
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
    
    chunk = await chunk_service.get_chunk(chunk_id)
    if not chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chunk with ID {chunk_id} not found"
        )
    
    # Verify chunk belongs to document
    if chunk.document_id != document_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chunk with ID {chunk_id} not found in document {document_id}"
        )
    
    return chunk


@router.put("/{chunk_id}", response_model=Chunk)
async def update_chunk(library_id: UUID, document_id: UUID, chunk_id: UUID, chunk_data: ChunkUpdate):
    """
    Update a chunk.
    
    Args:
        library_id: Library ID
        document_id: Document ID
        chunk_id: Chunk ID
        chunk_data: Chunk update data
        
    Returns:
        Updated chunk
        
    Raises:
        HTTPException: If library, document, or chunk not found
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
    
    chunk = await chunk_service.update_chunk(chunk_id, chunk_data)
    if not chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chunk with ID {chunk_id} not found"
        )
    
    # Verify chunk belongs to document
    if chunk.document_id != document_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chunk with ID {chunk_id} not found in document {document_id}"
        )
    
    return chunk


@router.delete("/{chunk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chunk(library_id: UUID, document_id: UUID, chunk_id: UUID):
    """
    Delete a chunk.
    
    Args:
        library_id: Library ID
        document_id: Document ID
        chunk_id: Chunk ID
        
    Raises:
        HTTPException: If library, document, or chunk not found
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
    
    # Check if chunk exists and belongs to document
    chunk = await chunk_service.get_chunk(chunk_id)
    if not chunk or chunk.document_id != document_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chunk with ID {chunk_id} not found in document {document_id}"
        )
    
    deleted = await chunk_service.delete_chunk(chunk_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chunk with ID {chunk_id} not found"
        )
    
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None
    )
