"""Integration tests for service/API flows and cascade operations."""

from uuid import uuid4

import pytest

from app.models import ChunkCreate, DocumentCreate, LibraryCreate
from app.repositories.base_repository import (
    InMemoryChunkRepository,
    InMemoryDocumentRepository,
    InMemoryLibraryRepository,
)
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService
from app.services.library_service import LibraryService
from app.services.search_service import SearchService


class TestCascadeOperations:
    """Test cascade delete operations."""
    
    @pytest.fixture
    async def setup_services(self):
        """Set up services with fresh repositories."""
        library_repo = InMemoryLibraryRepository()
        document_repo = InMemoryDocumentRepository()
        chunk_repo = InMemoryChunkRepository()
        
        chunk_service = ChunkService(chunk_repo, document_repo)
        document_service = DocumentService(document_repo, library_repo)
        library_service = LibraryService(library_repo)
        search_service = SearchService(chunk_service)
        
        # Inject dependencies
        document_service.set_chunk_service(chunk_service)
        document_service.set_search_service(search_service)
        library_service.set_document_service(document_service)
        library_service.set_search_service(search_service)
        
        return {
            'library_service': library_service,
            'document_service': document_service,
            'chunk_service': chunk_service,
            'search_service': search_service,
            'library_repo': library_repo,
            'document_repo': document_repo,
            'chunk_repo': chunk_repo
        }
    
    @pytest.mark.asyncio
    async def test_document_cascade_delete(self, setup_services):
        """Test that deleting a document removes all its chunks."""
        services = await setup_services
        
        # Create library
        library_data = LibraryCreate(name="Test Library", description="Test")
        library = await services['library_service'].create_library(library_data)
        
        # Create document
        document_data = DocumentCreate(title="Test Doc", content="Test content")
        document = await services['document_service'].create_document(library.id, document_data)
        
        # Create chunks
        chunk1_data = ChunkCreate(text="Chunk 1", metadata={"test": "1"})
        chunk2_data = ChunkCreate(text="Chunk 2", metadata={"test": "2"})
        
        chunk1 = await services['chunk_service'].create_chunk(document.id, chunk1_data)
        chunk2 = await services['chunk_service'].create_chunk(document.id, chunk2_data)
        
        # Verify chunks exist
        chunks = await services['chunk_service'].get_chunks_by_document(document.id)
        assert len(chunks) == 2
        
        # Delete document
        deleted = await services['document_service'].delete_document(document.id)
        assert deleted is True
        
        # Verify document is deleted
        document_check = await services['document_service'].get_document(document.id)
        assert document_check is None
        
        # Verify chunks are deleted
        chunks_after = await services['chunk_service'].get_chunks_by_document(document.id)
        assert len(chunks_after) == 0
        
        # Verify chunks don't exist individually
        chunk1_check = await services['chunk_service'].get_chunk(chunk1.id)
        chunk2_check = await services['chunk_service'].get_chunk(chunk2.id)
        assert chunk1_check is None
        assert chunk2_check is None
    
    @pytest.mark.asyncio
    async def test_library_cascade_delete(self, setup_services):
        """Test that deleting a library removes all documents and chunks."""
        services = await setup_services
        
        # Create library
        library_data = LibraryCreate(name="Test Library", description="Test")
        library = await services['library_service'].create_library(library_data)
        
        # Create documents
        doc1_data = DocumentCreate(title="Doc 1", content="Content 1")
        doc2_data = DocumentCreate(title="Doc 2", content="Content 2")
        
        doc1 = await services['document_service'].create_document(library.id, doc1_data)
        doc2 = await services['document_service'].create_document(library.id, doc2_data)
        
        # Create chunks
        chunk1_data = ChunkCreate(text="Chunk 1", metadata={"doc": "1"})
        chunk2_data = ChunkCreate(text="Chunk 2", metadata={"doc": "2"})
        
        chunk1 = await services['chunk_service'].create_chunk(doc1.id, chunk1_data)
        chunk2 = await services['chunk_service'].create_chunk(doc2.id, chunk2_data)
        
        # Verify data exists
        documents = await services['document_service'].get_documents_by_library(library.id)
        assert len(documents) == 2
        
        chunks = await services['chunk_service'].get_chunks_by_library(library.id)
        assert len(chunks) == 2
        
        # Delete library
        deleted = await services['library_service'].delete_library(library.id)
        assert deleted is True
        
        # Verify library is deleted
        library_check = await services['library_service'].get_library(library.id)
        assert library_check is None
        
        # Verify documents are deleted
        documents_after = await services['document_service'].get_documents_by_library(library.id)
        assert len(documents_after) == 0
        
        # Verify chunks are deleted
        chunks_after = await services['chunk_service'].get_chunks_by_library(library.id)
        assert len(chunks_after) == 0
    
    @pytest.mark.asyncio
    async def test_aggregate_data_updates(self, setup_services):
        """Test that aggregate data is properly updated."""
        services = await setup_services
        
        # Create library
        library_data = LibraryCreate(name="Test Library", description="Test")
        library = await services['library_service'].create_library(library_data)
        
        # Verify library has empty documents list initially
        assert len(library.documents) == 0
        
        # Create document
        document_data = DocumentCreate(title="Test Doc", content="Test content")
        document = await services['document_service'].create_document(library.id, document_data)
        
        # Verify document is added to library's documents list
        updated_library = await services['library_service'].get_library(library.id)
        assert len(updated_library.documents) == 1
        assert updated_library.documents[0].id == document.id
        
        # Verify document has empty chunks list initially
        assert len(document.chunks) == 0
        
        # Create chunk
        chunk_data = ChunkCreate(text="Test chunk", metadata={"test": "true"})
        chunk = await services['chunk_service'].create_chunk(document.id, chunk_data)
        
        # Verify chunk is added to document's chunks list
        updated_document = await services['document_service'].get_document(document.id)
        assert len(updated_document.chunks) == 1
        assert updated_document.chunks[0].id == chunk.id
    
    @pytest.mark.asyncio
    async def test_timestamp_updates(self, setup_services):
        """Test that timestamps are updated on modifications."""
        import time
        
        services = await setup_services
        
        # Create library
        library_data = LibraryCreate(name="Test Library", description="Test")
        library = await services['library_service'].create_library(library_data)
        original_updated_at = library.updated_at
        
        # Wait a moment
        time.sleep(0.1)
        
        # Update library
        from app.models import LibraryUpdate
        update_data = LibraryUpdate(description="Updated description")
        updated_library = await services['library_service'].update_library(library.id, update_data)
        
        # Verify timestamp was updated
        assert updated_library.updated_at > original_updated_at
        
        # Create document
        document_data = DocumentCreate(title="Test Doc", content="Test content")
        document = await services['document_service'].create_document(library.id, document_data)
        original_doc_updated_at = document.updated_at
        
        # Wait a moment
        time.sleep(0.1)
        
        # Update document
        from app.models import DocumentUpdate
        doc_update_data = DocumentUpdate(title="Updated Title")
        updated_document = await services['document_service'].update_document(document.id, doc_update_data)
        
        # Verify timestamp was updated
        assert updated_document.updated_at > original_doc_updated_at


class TestSearchIndexConsistency:
    """Test search index consistency after cascade operations."""
    
    @pytest.fixture
    async def setup_services(self):
        """Set up services with fresh repositories."""
        library_repo = InMemoryLibraryRepository()
        document_repo = InMemoryDocumentRepository()
        chunk_repo = InMemoryChunkRepository()
        
        chunk_service = ChunkService(chunk_repo, document_repo)
        document_service = DocumentService(document_repo, library_repo)
        library_service = LibraryService(library_repo)
        search_service = SearchService(chunk_service)
        
        # Inject dependencies
        document_service.set_chunk_service(chunk_service)
        document_service.set_search_service(search_service)
        library_service.set_document_service(document_service)
        library_service.set_search_service(search_service)
        
        return {
            'library_service': library_service,
            'document_service': document_service,
            'chunk_service': chunk_service,
            'search_service': search_service,
        }
    
    @pytest.mark.asyncio
    async def test_search_index_cleared_after_document_delete(self, setup_services):
        """Test that search indexes are cleared after document deletion."""
        services = await setup_services
        
        # Create library and document with chunks
        library_data = LibraryCreate(name="Test Library", description="Test")
        library = await services['library_service'].create_library(library_data)
        
        document_data = DocumentCreate(title="Test Doc", content="Test content")
        document = await services['document_service'].create_document(library.id, document_data)
        
        chunk_data = ChunkCreate(text="Test chunk", metadata={"test": "true"})
        await services['chunk_service'].create_chunk(document.id, chunk_data)
        
        # Build search index
        await services['search_service'].build_flat_index(library.id)
        
        # Verify index exists
        stats = await services['search_service'].get_index_stats(library.id)
        assert stats['flat_index'] is not None
        
        # Delete document (should clear indexes)
        await services['document_service'].delete_document(document.id)
        
        # Verify index is cleared
        stats_after = await services['search_service'].get_index_stats(library.id)
        assert stats_after['flat_index'] is None
    
    @pytest.mark.asyncio
    async def test_search_index_cleared_after_library_delete(self, setup_services):
        """Test that search indexes are cleared after library deletion."""
        services = await setup_services
        
        # Create library with documents and chunks
        library_data = LibraryCreate(name="Test Library", description="Test")
        library = await services['library_service'].create_library(library_data)
        
        document_data = DocumentCreate(title="Test Doc", content="Test content")
        document = await services['document_service'].create_document(library.id, document_data)
        
        chunk_data = ChunkCreate(text="Test chunk", metadata={"test": "true"})
        await services['chunk_service'].create_chunk(document.id, chunk_data)
        
        # Build search indexes
        await services['search_service'].build_flat_index(library.id)
        await services['search_service'].build_ivf_index(library.id)
        
        # Verify indexes exist
        stats = await services['search_service'].get_index_stats(library.id)
        assert stats['flat_index'] is not None
        assert stats['ivf_index'] is not None
        
        # Delete library (should clear indexes)
        await services['library_service'].delete_library(library.id)
        
        # Verify indexes are cleared
        stats_after = await services['search_service'].get_index_stats(library.id)
        assert stats_after['flat_index'] is None
        assert stats_after['ivf_index'] is None
