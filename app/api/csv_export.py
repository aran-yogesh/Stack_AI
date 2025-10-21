"""CSV export endpoints for data visualization."""

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.models import Chunk, Document, Library
from app.repositories.shared import (
    chunk_repository,
    document_repository,
    library_repository,
)
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService
from app.services.library_service import LibraryService
from app.utils.csv_storage import csv_storage

# Initialize router
router = APIRouter(prefix="/export", tags=["csv-export"])

# Initialize services
chunk_service = ChunkService(chunk_repository, document_repository)
document_service = DocumentService(document_repository, library_repository)
library_service = LibraryService(library_repository)


@router.get("/libraries/csv")
async def export_libraries_csv():
    """Export all libraries to CSV."""
    try:
        libraries = await library_service.get_all_libraries()
        filename = csv_storage.save_libraries(libraries)
        return FileResponse(
            filename,
            media_type="text/csv",
            filename=f"libraries_{len(libraries)}_items.csv"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export libraries: {str(e)}"
        )


@router.get("/documents/csv")
async def export_documents_csv():
    """Export all documents to CSV."""
    try:
        documents = await document_service.get_all_documents()
        filename = csv_storage.save_documents(documents)
        return FileResponse(
            filename,
            media_type="text/csv",
            filename=f"documents_{len(documents)}_items.csv"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export documents: {str(e)}"
        )


@router.get("/chunks/csv")
async def export_chunks_csv():
    """Export all chunks with embeddings to CSV."""
    try:
        chunks = await chunk_service.get_all_chunks()
        filename = csv_storage.save_chunks_with_embeddings(chunks)
        return FileResponse(
            filename,
            media_type="text/csv",
            filename=f"chunks_{len(chunks)}_items.csv"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export chunks: {str(e)}"
        )


@router.get("/embeddings/full/csv")
async def export_full_embeddings_csv():
    """Export full embeddings to CSV (one row per chunk, columns for each dimension)."""
    try:
        chunks = await chunk_service.get_all_chunks()
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No chunks found to export"
            )
        
        filename = csv_storage.save_full_embeddings(chunks)
        return FileResponse(
            filename,
            media_type="text/csv",
            filename=f"full_embeddings_{len(chunks)}_items.csv"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export embeddings: {str(e)}"
        )


@router.get("/library/{library_id}/chunks/csv")
async def export_library_chunks_csv(library_id: UUID):
    """Export chunks from a specific library to CSV."""
    try:
        chunks = await chunk_service.get_chunks_with_embeddings(library_id)
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No chunks found in library {library_id}"
            )
        
        filename = csv_storage.save_chunks_with_embeddings(chunks)
        return FileResponse(
            filename,
            media_type="text/csv",
            filename=f"library_{library_id}_chunks_{len(chunks)}_items.csv"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export library chunks: {str(e)}"
        )


@router.get("/summary/report")
async def export_summary_report():
    """Export a summary report of all data."""
    try:
        libraries = await library_service.get_all_libraries()
        documents = await document_service.get_all_documents()
        chunks = await chunk_service.get_all_chunks()
        
        filename = csv_storage.create_summary_report(libraries, documents, chunks)
        return FileResponse(
            filename,
            media_type="text/plain",
            filename="vector_database_summary.txt"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create summary report: {str(e)}"
        )


@router.get("/all/csv")
async def export_all_data_csv():
    """Export all data (libraries, documents, chunks) to separate CSV files."""
    try:
        libraries = await library_service.get_all_libraries()
        documents = await document_service.get_all_documents()
        chunks = await chunk_service.get_all_chunks()
        
        files_created = []
        
        if libraries:
            lib_file = csv_storage.save_libraries(libraries)
            files_created.append(f"Libraries: {lib_file}")
        
        if documents:
            doc_file = csv_storage.save_documents(documents)
            files_created.append(f"Documents: {doc_file}")
        
        if chunks:
            chunk_file = csv_storage.save_chunks_with_embeddings(chunks)
            files_created.append(f"Chunks: {chunk_file}")
            
            # Also create full embeddings file
            embedding_file = csv_storage.save_full_embeddings(chunks)
            files_created.append(f"Full Embeddings: {embedding_file}")
        
        summary_file = csv_storage.create_summary_report(libraries, documents, chunks)
        files_created.append(f"Summary Report: {summary_file}")
        
        return {
            "message": "All data exported successfully",
            "files_created": files_created,
            "counts": {
                "libraries": len(libraries),
                "documents": len(documents),
                "chunks": len(chunks)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export all data: {str(e)}"
        )
