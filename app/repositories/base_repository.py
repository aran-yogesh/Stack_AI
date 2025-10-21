"""Base repository interface and implementations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar
from uuid import UUID

from app.models import Chunk, Document, Library
from app.utils.concurrency import ThreadSafeDict, ThreadSafeList

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository class."""
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> Optional[T]:
        """Get entity by ID."""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[T]:
        """Get all entities."""
        pass
    
    @abstractmethod
    async def update(self, entity: T) -> Optional[T]:
        """Update an entity."""
        pass
    
    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        """Delete an entity by ID."""
        pass
    
    @abstractmethod
    async def exists(self, entity_id: UUID) -> bool:
        """Check if entity exists."""
        pass


class InMemoryLibraryRepository(BaseRepository[Library]):
    """In-memory repository for Library entities."""
    
    def __init__(self):
        self._libraries: ThreadSafeDict[UUID, Library] = ThreadSafeDict()
    
    async def create(self, library: Library) -> Library:
        """Create a new library."""
        self._libraries.set(library.id, library)
        return library
    
    async def get_by_id(self, library_id: UUID) -> Optional[Library]:
        """Get library by ID."""
        return self._libraries.get(library_id)
    
    async def get_all(self) -> List[Library]:
        """Get all libraries."""
        return self._libraries.values()
    
    async def update(self, library: Library) -> Optional[Library]:
        """Update a library."""
        if library.id in self._libraries:
            self._libraries.set(library.id, library)
            return library
        return None
    
    async def delete(self, library_id: UUID) -> bool:
        """Delete a library by ID."""
        return self._libraries.delete(library_id)
    
    async def exists(self, library_id: UUID) -> bool:
        """Check if library exists."""
        return library_id in self._libraries


class InMemoryDocumentRepository(BaseRepository[Document]):
    """In-memory repository for Document entities."""
    
    def __init__(self):
        self._documents: ThreadSafeDict[UUID, Document] = ThreadSafeDict()
        self._library_documents: ThreadSafeDict[UUID, ThreadSafeList[UUID]] = ThreadSafeDict()
    
    async def create(self, document: Document) -> Document:
        """Create a new document."""
        self._documents.set(document.id, document)
        
        # Add to library's document list
        if document.library_id not in self._library_documents:
            self._library_documents.set(document.library_id, ThreadSafeList())
        self._library_documents.get(document.library_id).append(document.id)
        
        return document
    
    async def get_by_id(self, document_id: UUID) -> Optional[Document]:
        """Get document by ID."""
        return self._documents.get(document_id)
    
    async def get_all(self) -> List[Document]:
        """Get all documents."""
        return self._documents.values()
    
    async def get_by_library_id(self, library_id: UUID) -> List[Document]:
        """Get all documents in a library."""
        document_ids = self._library_documents.get(library_id, ThreadSafeList())
        documents = []
        for doc_id in document_ids:
            doc = self._documents.get(doc_id)
            if doc:
                documents.append(doc)
        return documents
    
    async def update(self, document: Document) -> Optional[Document]:
        """Update a document."""
        if document.id in self._documents:
            self._documents.set(document.id, document)
            return document
        return None
    
    async def delete(self, document_id: UUID) -> bool:
        """Delete a document by ID."""
        document = self._documents.get(document_id)
        if document:
            # Remove from library's document list
            library_docs = self._library_documents.get(document.library_id)
            if library_docs:
                library_docs.remove(document_id)
            
            # Delete the document
            return self._documents.delete(document_id)
        return False
    
    async def exists(self, document_id: UUID) -> bool:
        """Check if document exists."""
        return document_id in self._documents


class InMemoryChunkRepository(BaseRepository[Chunk]):
    """In-memory repository for Chunk entities."""
    
    def __init__(self):
        self._chunks: ThreadSafeDict[UUID, Chunk] = ThreadSafeDict()
        self._document_chunks: ThreadSafeDict[UUID, ThreadSafeList[UUID]] = ThreadSafeDict()
        self._library_chunks: ThreadSafeDict[UUID, ThreadSafeList[UUID]] = ThreadSafeDict()
    
    async def create(self, chunk: Chunk) -> Chunk:
        """Create a new chunk."""
        self._chunks.set(chunk.id, chunk)
        
        # Add to document's chunk list
        if chunk.document_id not in self._document_chunks:
            self._document_chunks.set(chunk.document_id, ThreadSafeList())
        self._document_chunks.get(chunk.document_id).append(chunk.id)
        
        return chunk
    
    async def get_by_id(self, chunk_id: UUID) -> Optional[Chunk]:
        """Get chunk by ID."""
        return self._chunks.get(chunk_id)
    
    async def get_all(self) -> List[Chunk]:
        """Get all chunks."""
        return self._chunks.values()
    
    async def get_by_document_id(self, document_id: UUID) -> List[Chunk]:
        """Get all chunks in a document."""
        chunk_ids = self._document_chunks.get(document_id, ThreadSafeList())
        chunks = []
        for chunk_id in chunk_ids:
            chunk = self._chunks.get(chunk_id)
            if chunk:
                chunks.append(chunk)
        return chunks
    
    async def get_by_library_id(self, library_id: UUID) -> List[Chunk]:
        """Get all chunks in a library."""
        chunk_ids = self._library_chunks.get(library_id, ThreadSafeList())
        chunks = []
        for chunk_id in chunk_ids:
            chunk = self._chunks.get(chunk_id)
            if chunk:
                chunks.append(chunk)
        return chunks
    
    async def get_chunks_with_embeddings(self, library_id: UUID) -> List[Chunk]:
        """Get all chunks with embeddings in a library."""
        chunks = await self.get_by_library_id(library_id)
        return [chunk for chunk in chunks if chunk.embedding is not None]
    
    async def update(self, chunk: Chunk) -> Optional[Chunk]:
        """Update a chunk."""
        if chunk.id in self._chunks:
            self._chunks.set(chunk.id, chunk)
            return chunk
        return None
    
    async def delete(self, chunk_id: UUID) -> bool:
        """Delete a chunk by ID."""
        chunk = self._chunks.get(chunk_id)
        if chunk:
            # Remove from document's chunk list
            doc_chunks = self._document_chunks.get(chunk.document_id)
            if doc_chunks:
                doc_chunks.remove(chunk_id)
            
            # Delete the chunk
            return self._chunks.delete(chunk_id)
        return False
    
    async def exists(self, chunk_id: UUID) -> bool:
        """Check if chunk exists."""
        return chunk_id in self._chunks
    
    async def add_to_library(self, chunk_id: UUID, library_id: UUID) -> None:
        """Add chunk to library's chunk list."""
        if library_id not in self._library_chunks:
            self._library_chunks.set(library_id, ThreadSafeList())
        self._library_chunks.get(library_id).append(chunk_id)
    
    async def remove_from_library(self, chunk_id: UUID, library_id: UUID) -> None:
        """Remove chunk from library's chunk list."""
        library_chunks = self._library_chunks.get(library_id)
        if library_chunks:
            library_chunks.remove(chunk_id)
