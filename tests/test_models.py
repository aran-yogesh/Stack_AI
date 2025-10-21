"""Unit tests for models."""

from datetime import datetime
from uuid import uuid4

import pytest

from app.models import (
    Chunk,
    ChunkCreate,
    ChunkUpdate,
    Document,
    DocumentCreate,
    DocumentUpdate,
    Library,
    LibraryCreate,
    LibraryUpdate,
    SearchQuery,
    SearchResponse,
    SearchResult,
)


class TestLibraryModels:
    """Test cases for Library models."""
    
    def test_library_create(self):
        """Test LibraryCreate model."""
        data = {
            "name": "Test Library",
            "description": "A test library",
            "metadata": {"category": "test"}
        }
        library_create = LibraryCreate(**data)
        assert library_create.name == "Test Library"
        assert library_create.description == "A test library"
        assert library_create.metadata == {"category": "test"}
    
    def test_library_update(self):
        """Test LibraryUpdate model."""
        data = {
            "name": "Updated Library",
            "metadata": {"category": "updated"}
        }
        library_update = LibraryUpdate(**data)
        assert library_update.name == "Updated Library"
        assert library_update.description is None
        assert library_update.metadata == {"category": "updated"}
    
    def test_library_model(self):
        """Test Library model."""
        library_id = uuid4()
        library = Library(
            id=library_id,
            name="Test Library",
            description="A test library",
            metadata={"category": "test"}
        )
        assert library.id == library_id
        assert library.name == "Test Library"
        assert library.description == "A test library"
        assert library.metadata == {"category": "test"}
        assert isinstance(library.created_at, datetime)
        assert isinstance(library.updated_at, datetime)


class TestDocumentModels:
    """Test cases for Document models."""
    
    def test_document_create(self):
        """Test DocumentCreate model."""
        data = {
            "title": "Test Document",
            "content": "This is test content",
            "metadata": {"author": "test"}
        }
        document_create = DocumentCreate(**data)
        assert document_create.title == "Test Document"
        assert document_create.content == "This is test content"
        assert document_create.metadata == {"author": "test"}
    
    def test_document_update(self):
        """Test DocumentUpdate model."""
        data = {
            "title": "Updated Document",
            "content": "Updated content"
        }
        document_update = DocumentUpdate(**data)
        assert document_update.title == "Updated Document"
        assert document_update.content == "Updated content"
        assert document_update.metadata is None
    
    def test_document_model(self):
        """Test Document model."""
        document_id = uuid4()
        library_id = uuid4()
        document = Document(
            id=document_id,
            library_id=library_id,
            title="Test Document",
            content="This is test content",
            metadata={"author": "test"}
        )
        assert document.id == document_id
        assert document.library_id == library_id
        assert document.title == "Test Document"
        assert document.content == "This is test content"
        assert document.metadata == {"author": "test"}
        assert isinstance(document.created_at, datetime)
        assert isinstance(document.updated_at, datetime)


class TestChunkModels:
    """Test cases for Chunk models."""
    
    def test_chunk_create(self):
        """Test ChunkCreate model."""
        data = {
            "text": "This is a test chunk",
            "metadata": {"type": "paragraph"}
        }
        chunk_create = ChunkCreate(**data)
        assert chunk_create.text == "This is a test chunk"
        assert chunk_create.metadata == {"type": "paragraph"}
    
    def test_chunk_update(self):
        """Test ChunkUpdate model."""
        data = {
            "text": "Updated chunk text",
            "metadata": {"type": "updated"}
        }
        chunk_update = ChunkUpdate(**data)
        assert chunk_update.text == "Updated chunk text"
        assert chunk_update.metadata == {"type": "updated"}
    
    def test_chunk_model(self):
        """Test Chunk model."""
        chunk_id = uuid4()
        document_id = uuid4()
        embedding = [0.1, 0.2, 0.3]
        
        chunk = Chunk(
            id=chunk_id,
            document_id=document_id,
            text="This is a test chunk",
            embedding=embedding,
            metadata={"type": "paragraph"}
        )
        assert chunk.id == chunk_id
        assert chunk.document_id == document_id
        assert chunk.text == "This is a test chunk"
        assert chunk.embedding == embedding
        assert chunk.metadata == {"type": "paragraph"}
        assert isinstance(chunk.created_at, datetime)
        assert isinstance(chunk.updated_at, datetime)


class TestSearchModels:
    """Test cases for Search models."""
    
    def test_search_query(self):
        """Test SearchQuery model."""
        query = SearchQuery(
            query_text="test query",
            k=5,
            metadata_filter={"author": "test"}
        )
        assert query.query_text == "test query"
        assert query.k == 5
        assert query.metadata_filter == {"author": "test"}
    
    def test_search_result(self):
        """Test SearchResult model."""
        chunk_id = uuid4()
        document_id = uuid4()
        chunk = Chunk(
            id=chunk_id,
            document_id=document_id,
            text="Test chunk",
            metadata={"type": "test"}
        )
        
        result = SearchResult(
            chunk=chunk,
            similarity_score=0.95,
            rank=1
        )
        assert result.chunk == chunk
        assert result.similarity_score == 0.95
        assert result.rank == 1
    
    def test_search_response(self):
        """Test SearchResponse model."""
        chunk_id = uuid4()
        document_id = uuid4()
        chunk = Chunk(
            id=chunk_id,
            document_id=document_id,
            text="Test chunk",
            metadata={"type": "test"}
        )
        
        result = SearchResult(
            chunk=chunk,
            similarity_score=0.95,
            rank=1
        )
        
        response = SearchResponse(
            query="test query",
            results=[result],
            total_results=1,
            search_time_ms=10.5
        )
        assert response.query == "test query"
        assert len(response.results) == 1
        assert response.total_results == 1
        assert response.search_time_ms == 10.5


class TestModelValidation:
    """Test model validation."""
    
    def test_library_name_validation(self):
        """Test library name validation."""
        # Test empty name
        with pytest.raises(ValueError):
            LibraryCreate(name="")
        
        # Test name too long
        with pytest.raises(ValueError):
            LibraryCreate(name="x" * 101)
    
    def test_document_title_validation(self):
        """Test document title validation."""
        # Test empty title
        with pytest.raises(ValueError):
            DocumentCreate(title="")
        
        # Test title too long
        with pytest.raises(ValueError):
            DocumentCreate(title="x" * 201)
    
    def test_chunk_text_validation(self):
        """Test chunk text validation."""
        # Test empty text
        with pytest.raises(ValueError):
            ChunkCreate(text="")
        
        # Test text too long
        with pytest.raises(ValueError):
            ChunkCreate(text="x" * 1001)
    
    def test_search_query_validation(self):
        """Test search query validation."""
        # Test empty query
        with pytest.raises(ValueError):
            SearchQuery(query_text="")
        
        # Test k too small
        with pytest.raises(ValueError):
            SearchQuery(query_text="test", k=0)
        
        # Test k too large
        with pytest.raises(ValueError):
            SearchQuery(query_text="test", k=101)
    
    def test_search_result_validation(self):
        """Test search result validation."""
        chunk_id = uuid4()
        document_id = uuid4()
        chunk = Chunk(
            id=chunk_id,
            document_id=document_id,
            text="Test chunk"
        )
        
        # Test similarity score too low
        with pytest.raises(ValueError):
            SearchResult(chunk=chunk, similarity_score=-0.1, rank=1)
        
        # Test similarity score too high
        with pytest.raises(ValueError):
            SearchResult(chunk=chunk, similarity_score=1.1, rank=1)
        
        # Test rank too low
        with pytest.raises(ValueError):
            SearchResult(chunk=chunk, similarity_score=0.5, rank=0)
