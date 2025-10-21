"""Library service for business logic operations."""

from typing import List, Optional
from uuid import UUID

from app.models import Library, LibraryCreate, LibraryUpdate
from app.repositories.base_repository import InMemoryLibraryRepository


class LibraryService:
    """Service for library business logic."""
    
    def __init__(self, repository: InMemoryLibraryRepository):
        self.repository = repository
        self._document_service = None  # Will be injected to avoid circular dependency
        self._search_service = None  # Will be injected to avoid circular dependency
    
    def set_document_service(self, document_service):
        """Set document service for cascade operations."""
        self._document_service = document_service
    
    def set_search_service(self, search_service):
        """Set search service for index invalidation."""
        self._search_service = search_service
    
    async def create_library(self, library_data: LibraryCreate) -> Library:
        """
        Create a new library.
        
        Args:
            library_data: Library creation data
            
        Returns:
            Created library
            
        Raises:
            ValueError: If library name already exists
        """
        # Check if library with same name already exists
        existing_libraries = await self.repository.get_all()
        for lib in existing_libraries:
            if lib.name == library_data.name:
                raise ValueError(f"Library with name '{library_data.name}' already exists")
        
        # Create new library
        library = Library(
            name=library_data.name,
            description=library_data.description,
            metadata=library_data.metadata
        )
        
        return await self.repository.create(library)
    
    async def get_library(self, library_id: UUID) -> Optional[Library]:
        """
        Get a library by ID.
        
        Args:
            library_id: Library ID
            
        Returns:
            Library if found, None otherwise
        """
        return await self.repository.get_by_id(library_id)
    
    async def get_all_libraries(self) -> List[Library]:
        """
        Get all libraries.
        
        Returns:
            List of all libraries
        """
        return await self.repository.get_all()
    
    async def update_library(self, library_id: UUID, library_data: LibraryUpdate) -> Optional[Library]:
        """
        Update a library.
        
        Args:
            library_id: Library ID
            library_data: Library update data
            
        Returns:
            Updated library if found, None otherwise
            
        Raises:
            ValueError: If library name already exists
        """
        library = await self.repository.get_by_id(library_id)
        if not library:
            return None
        
        # Check if new name conflicts with existing libraries
        if library_data.name and library_data.name != library.name:
            existing_libraries = await self.repository.get_all()
            for lib in existing_libraries:
                if lib.id != library_id and lib.name == library_data.name:
                    raise ValueError(f"Library with name '{library_data.name}' already exists")
        
        # Update fields
        if library_data.name is not None:
            library.name = library_data.name
        if library_data.description is not None:
            library.description = library_data.description
        if library_data.metadata is not None:
            library.metadata = library_data.metadata
        
        # Update timestamp
        from datetime import datetime
        library.updated_at = datetime.utcnow()
        
        return await self.repository.update(library)
    
    async def delete_library(self, library_id: UUID) -> bool:
        """
        Delete a library and all its documents and chunks (cascade delete).
        
        Args:
            library_id: Library ID
            
        Returns:
            True if deleted, False if not found
        """
        library = await self.repository.get_by_id(library_id)
        if not library:
            return False
        
        # Cascade delete: Remove all documents (which will cascade to chunks)
        if self._document_service:
            documents = await self._document_service.get_documents_by_library(library_id)
            deleted_documents = 0
            for document in documents:
                if await self._document_service.delete_document(document.id):
                    deleted_documents += 1
            print(f"Deleted {deleted_documents} documents for library {library_id}")
        
        # Clear search indexes for the library
        if self._search_service:
            try:
                await self._search_service.clear_indexes(library_id)
            except Exception as e:
                print(f"Warning: Failed to clear search indexes for library {library_id}: {e}")
        
        # Delete the library
        return await self.repository.delete(library_id)
    
    async def library_exists(self, library_id: UUID) -> bool:
        """
        Check if a library exists.
        
        Args:
            library_id: Library ID
            
        Returns:
            True if exists, False otherwise
        """
        return await self.repository.exists(library_id)
