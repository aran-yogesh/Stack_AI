"""Shared repository instances for the application."""

from app.repositories.base_repository import (
    InMemoryChunkRepository,
    InMemoryDocumentRepository,
    InMemoryLibraryRepository,
)

# Global shared repository instances
library_repository = InMemoryLibraryRepository()
document_repository = InMemoryDocumentRepository()
chunk_repository = InMemoryChunkRepository()
