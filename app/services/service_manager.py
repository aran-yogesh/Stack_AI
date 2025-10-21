"""Service dependency injection manager."""

from app.repositories.shared import (
    chunk_repository,
    document_repository,
    library_repository,
)
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService
from app.services.library_service import LibraryService
from app.services.search_service import SearchService


class ServiceManager:
    """Manages service dependencies and injection."""
    
    def __init__(self):
        # Initialize services
        self.chunk_service = ChunkService(chunk_repository, document_repository)
        self.document_service = DocumentService(
            document_repository, library_repository
        )
        self.library_service = LibraryService(library_repository)
        self.search_service = SearchService(self.chunk_service)

        # Inject dependencies
        self._setup_dependencies()

    def _setup_dependencies(self):
        """Set up service dependencies to avoid circular imports."""
        # Document service needs chunk service and search service
        self.document_service.set_chunk_service(self.chunk_service)
        self.document_service.set_search_service(self.search_service)

        # Library service needs document service and search service
        self.library_service.set_document_service(self.document_service)
        self.library_service.set_search_service(self.search_service)


# Global service manager instance
service_manager = ServiceManager()
