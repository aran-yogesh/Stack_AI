"""Chunk service for business logic operations."""

from typing import List, Optional
from uuid import UUID

from app.models import Chunk, ChunkCreate, ChunkUpdate
from app.repositories.base_repository import (
    InMemoryChunkRepository,
    InMemoryDocumentRepository,
)
from app.services.embedding_service import embedding_service


class ChunkService:
    """Service for chunk business logic."""
    
    def __init__(self, chunk_repository: InMemoryChunkRepository, document_repository: InMemoryDocumentRepository):
        self.chunk_repository = chunk_repository
        self.document_repository = document_repository
    
    async def create_chunk(self, document_id: UUID, chunk_data: ChunkCreate) -> Chunk:
        """
        Create a new chunk in a document.
        
        Args:
            document_id: Parent document ID
            chunk_data: Chunk creation data
            
        Returns:
            Created chunk with embedding
            
        Raises:
            ValueError: If document doesn't exist
        """
        # Check if document exists
        document = await self.document_repository.get_by_id(document_id)
        if not document:
            raise ValueError(f"Document with ID {document_id} not found")
        
        # Generate embedding for the chunk text
        embedding = await embedding_service.get_embedding(chunk_data.text)
        
        # Create new chunk
        chunk = Chunk(
            text=chunk_data.text,
            metadata=chunk_data.metadata,
            document_id=document_id,
            embedding=embedding
        )
        
        # Add chunk to library's chunk list
        await self.chunk_repository.add_to_library(chunk.id, document.library_id)
        
        # Save chunk
        created_chunk = await self.chunk_repository.create(chunk)
        
        # Update document's chunks list
        document.chunks.append(created_chunk)
        await self.document_repository.update(document)
        
        return created_chunk
    
    async def get_chunk(self, chunk_id: UUID) -> Optional[Chunk]:
        """
        Get a chunk by ID.
        
        Args:
            chunk_id: Chunk ID
            
        Returns:
            Chunk if found, None otherwise
        """
        return await self.chunk_repository.get_by_id(chunk_id)
    
    async def get_chunks_by_document(self, document_id: UUID) -> List[Chunk]:
        """
        Get all chunks in a document.
        
        Args:
            document_id: Document ID
            
        Returns:
            List of chunks in the document
        """
        return await self.chunk_repository.get_by_document_id(document_id)
    
    async def get_chunks_by_library(self, library_id: UUID) -> List[Chunk]:
        """
        Get all chunks in a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            List of chunks in the library
        """
        return await self.chunk_repository.get_by_library_id(library_id)
    
    async def get_chunks_with_embeddings(self, library_id: UUID) -> List[Chunk]:
        """
        Get all chunks with embeddings in a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            List of chunks with embeddings
        """
        return await self.chunk_repository.get_chunks_with_embeddings(library_id)
    
    async def get_all_chunks(self) -> List[Chunk]:
        """
        Get all chunks.
        
        Returns:
            List of all chunks
        """
        return await self.chunk_repository.get_all()
    
    async def update_chunk(self, chunk_id: UUID, chunk_data: ChunkUpdate) -> Optional[Chunk]:
        """
        Update a chunk.
        
        Args:
            chunk_id: Chunk ID
            chunk_data: Chunk update data
            
        Returns:
            Updated chunk if found, None otherwise
        """
        chunk = await self.chunk_repository.get_by_id(chunk_id)
        if not chunk:
            return None
        
        # Update fields
        if chunk_data.text is not None:
            chunk.text = chunk_data.text
            # Regenerate embedding if text changed
            chunk.embedding = await embedding_service.get_embedding(chunk_data.text)
        
        if chunk_data.metadata is not None:
            chunk.metadata = chunk_data.metadata
        
        # Update timestamp
        from datetime import datetime
        chunk.updated_at = datetime.utcnow()
        
        return await self.chunk_repository.update(chunk)
    
    async def delete_chunk(self, chunk_id: UUID) -> bool:
        """
        Delete a chunk.
        
        Args:
            chunk_id: Chunk ID
            
        Returns:
            True if deleted, False if not found
        """
        chunk = await self.chunk_repository.get_by_id(chunk_id)
        if not chunk:
            return False
        
        # Get the document to update its chunks list
        document = await self.document_repository.get_by_id(chunk.document_id)
        if document:
            # Remove from library's chunk list
            await self.chunk_repository.remove_from_library(chunk_id, document.library_id)
            
            # Remove from document's chunks list
            document.chunks = [c for c in document.chunks if c.id != chunk_id]
            await self.document_repository.update(document)
        
        return await self.chunk_repository.delete(chunk_id)
    
    async def delete_chunks_by_document(self, document_id: UUID) -> int:
        """
        Delete all chunks belonging to a document.
        
        Args:
            document_id: Document ID
            
        Returns:
            Number of chunks deleted
        """
        chunks = await self.chunk_repository.get_by_document_id(document_id)
        deleted_count = 0
        
        # Get the library_id for cleanup
        document = await self.document_repository.get_by_id(document_id)
        library_id = document.library_id if document else None
        
        for chunk in chunks:
            # Remove from library's chunk list before deleting
            if library_id:
                await self.chunk_repository.remove_from_library(chunk.id, library_id)
            
            if await self.chunk_repository.delete(chunk.id):
                deleted_count += 1
        
        return deleted_count
    
    async def chunk_exists(self, chunk_id: UUID) -> bool:
        """
        Check if a chunk exists.
        
        Args:
            chunk_id: Chunk ID
            
        Returns:
            True if exists, False otherwise
        """
        return await self.chunk_repository.exists(chunk_id)
    
    async def regenerate_embeddings(self, library_id: UUID) -> int:
        """
        Regenerate embeddings for all chunks in a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            Number of chunks updated
        """
        chunks = await self.get_chunks_by_library(library_id)
        updated_count = 0
        
        for chunk in chunks:
            if chunk.text:
                chunk.embedding = await embedding_service.get_embedding(chunk.text)
                await self.chunk_repository.update(chunk)
                updated_count += 1
        
        return updated_count
