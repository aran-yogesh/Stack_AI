"""Pydantic models for the Vector Database."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ChunkBase(BaseModel):
    """Base model for Chunk."""
    text: str = Field(..., min_length=1, max_length=1000, description="The text content of the chunk")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the chunk")


class ChunkCreate(ChunkBase):
    """Model for creating a new chunk."""
    pass


class ChunkUpdate(BaseModel):
    """Model for updating a chunk."""
    text: Optional[str] = Field(None, min_length=1, max_length=1000)
    metadata: Optional[Dict[str, Any]] = None


class Chunk(ChunkBase):
    """Complete chunk model with all fields."""
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the chunk")
    document_id: UUID = Field(..., description="ID of the parent document")
    embedding: Optional[List[float]] = Field(None, description="Vector embedding of the chunk text")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DocumentBase(BaseModel):
    """Base model for Document."""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the document")
    content: Optional[str] = Field(None, description="Full content of the document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the document")


class DocumentCreate(DocumentBase):
    """Model for creating a new document."""
    pass


class DocumentUpdate(BaseModel):
    """Model for updating a document."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Document(DocumentBase):
    """Complete document model with all fields."""
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the document")
    library_id: UUID = Field(..., description="ID of the parent library")
    chunks: List[Chunk] = Field(default_factory=list, description="List of chunks in this document")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LibraryBase(BaseModel):
    """Base model for Library."""
    name: str = Field(..., min_length=1, max_length=100, description="Name of the library")
    description: Optional[str] = Field(None, max_length=500, description="Description of the library")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata for the library")


class LibraryCreate(LibraryBase):
    """Model for creating a new library."""
    pass


class LibraryUpdate(BaseModel):
    """Model for updating a library."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, Any]] = None


class Library(LibraryBase):
    """Complete library model with all fields."""
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the library")
    documents: List[Document] = Field(default_factory=list, description="List of documents in this library")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SearchQuery(BaseModel):
    """Model for k-NN search queries."""
    query_text: str = Field(..., min_length=1, description="Text to search for")
    k: int = Field(default=10, ge=1, le=100, description="Number of results to return")
    metadata_filter: Optional[Dict[str, Any]] = Field(None, description="Optional metadata filters")


class SearchResult(BaseModel):
    """Model for search results."""
    chunk: Chunk
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Cosine similarity score")
    rank: int = Field(..., ge=1, description="Rank of this result")


class SearchResponse(BaseModel):
    """Model for search response."""
    query: str
    results: List[SearchResult]
    total_results: int
    search_time_ms: float
