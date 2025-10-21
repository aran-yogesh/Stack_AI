"""Document service for business logic operations."""

from typing import List, Optional
from uuid import UUID

from app.models import Document, DocumentCreate, DocumentUpdate
from app.repositories.base_repository import (
    InMemoryDocumentRepository,
    InMemoryLibraryRepository,
)


class DocumentService:
    """Service for document business logic."""
    
    def __init__(self, document_repository: InMemoryDocumentRepository, library_repository: InMemoryLibraryRepository):
        self.document_repository = document_repository
        self.library_repository = library_repository
        self._chunk_service = None  # Will be injected to avoid circular dependency
        self._search_service = None  # Will be injected to avoid circular dependency
    
    def set_chunk_service(self, chunk_service):
        """Set chunk service for cascade operations."""
        self._chunk_service = chunk_service
    
    def set_search_service(self, search_service):
        """Set search service for index invalidation."""
        self._search_service = search_service
    
    async def create_document(self, library_id: UUID, document_data: DocumentCreate) -> Document:
        """
        Create a new document in a library.
        
        Args:
            library_id: Parent library ID
            document_data: Document creation data
            
        Returns:
            Created document
            
        Raises:
            ValueError: If library doesn't exist or document title already exists in library
        """
        # Check if library exists
        library = await self.library_repository.get_by_id(library_id)
        if not library:
            raise ValueError(f"Library with ID {library_id} not found")
        
        # Check if document with same title already exists in library
        existing_documents = await self.document_repository.get_by_library_id(library_id)
        for doc in existing_documents:
            if doc.title == document_data.title:
                raise ValueError(f"Document with title '{document_data.title}' already exists in library")
        
        # Create new document
        document = Document(
            title=document_data.title,
            content=document_data.content,
            metadata=document_data.metadata,
            library_id=library_id
        )
        
        # Save document
        created_document = await self.document_repository.create(document)
        
        # Update library's documents list
        library.documents.append(created_document)
        await self.library_repository.update(library)
        
        return created_document
    
    async def get_document(self, document_id: UUID) -> Optional[Document]:
        """
        Get a document by ID.
        
        Args:
            document_id: Document ID
            
        Returns:
            Document if found, None otherwise
        """
        return await self.document_repository.get_by_id(document_id)
    
    async def get_documents_by_library(self, library_id: UUID) -> List[Document]:
        """
        Get all documents in a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            List of documents in the library
        """
        return await self.document_repository.get_by_library_id(library_id)
    
    async def get_all_documents(self) -> List[Document]:
        """
        Get all documents.
        
        Returns:
            List of all documents
        """
        return await self.document_repository.get_all()
    
    async def update_document(self, document_id: UUID, document_data: DocumentUpdate) -> Optional[Document]:
        """
        Update a document.
        
        Args:
            document_id: Document ID
            document_data: Document update data
            
        Returns:
            Updated document if found, None otherwise
            
        Raises:
            ValueError: If document title already exists in library
        """
        document = await self.document_repository.get_by_id(document_id)
        if not document:
            return None
        
        # Check if new title conflicts with existing documents in the same library
        if document_data.title and document_data.title != document.title:
            existing_documents = await self.document_repository.get_by_library_id(document.library_id)
            for doc in existing_documents:
                if doc.id != document_id and doc.title == document_data.title:
                    raise ValueError(f"Document with title '{document_data.title}' already exists in library")
        
        # Update fields
        if document_data.title is not None:
            document.title = document_data.title
        if document_data.content is not None:
            document.content = document_data.content
        if document_data.metadata is not None:
            document.metadata = document_data.metadata
        
        # Update timestamp
        from datetime import datetime
        document.updated_at = datetime.utcnow()
        
        return await self.document_repository.update(document)
    
    async def delete_document(self, document_id: UUID) -> bool:
        """
        Delete a document and all its chunks (cascade delete).
        
        Args:
            document_id: Document ID
            
        Returns:
            True if deleted, False if not found
        """
        document = await self.document_repository.get_by_id(document_id)
        if not document:
            return False
        
        # Cascade delete: Remove all chunks belonging to this document
        if self._chunk_service:
            deleted_chunks = await self._chunk_service.delete_chunks_by_document(document_id)
            print(f"Deleted {deleted_chunks} chunks for document {document_id}")
        
        # Invalidate search indexes for the library
        if self._search_service:
            try:
                # Clear indexes for the library to prevent orphaned data in search results
                await self._search_service.clear_indexes(document.library_id)
            except Exception as e:
                print(f"Warning: Failed to clear search indexes for library {document.library_id}: {e}")
        
        # Remove document from library's documents list
        library = await self.library_repository.get_by_id(document.library_id)
        if library:
            library.documents = [doc for doc in library.documents if doc.id != document_id]
            await self.library_repository.update(library)
        
        # Delete the document
        return await self.document_repository.delete(document_id)
    
    async def document_exists(self, document_id: UUID) -> bool:
        """
        Check if a document exists.
        
        Args:
            document_id: Document ID
            
        Returns:
            True if exists, False otherwise
        """
        return await self.document_repository.exists(document_id)
