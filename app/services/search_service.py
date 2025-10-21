"""Search service for vector similarity search and indexing."""

import time
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.config import settings
from app.indexing.flat_index import FlatIndex
from app.indexing.ivf_index import IVFIndex
from app.models import Chunk, SearchQuery, SearchResponse, SearchResult
from app.services.chunk_service import ChunkService
from app.services.embedding_service import embedding_service


class SearchService:
    """Service for vector similarity search and indexing."""
    
    def __init__(self, chunk_service: ChunkService):
        self.chunk_service = chunk_service
        self.flat_indexes: Dict[UUID, FlatIndex] = {}
        self.ivf_indexes: Dict[UUID, IVFIndex] = {}
    
    async def build_indexes(self, library_id: UUID) -> Dict[str, Any]:
        """
        Build both Flat and IVF indexes for a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            Dictionary with build statistics
        """
        # Get all chunks with embeddings
        chunks = await self.chunk_service.get_chunks_with_embeddings(library_id)
        
        if not chunks:
            return {
                "message": "No chunks with embeddings found",
                "flat_index": None,
                "ivf_index": None
            }
        
        stats = {}
        
        # Build Flat Index
        flat_index = FlatIndex(settings.embedding_dimension)
        flat_index.add_vectors(chunks)
        flat_index.build()
        self.flat_indexes[library_id] = flat_index
        
        stats["flat_index"] = flat_index.get_stats()
        
        # Build IVF Index
        ivf_index = IVFIndex(settings.embedding_dimension)
        ivf_index.add_vectors(chunks)
        ivf_index.build()
        self.ivf_indexes[library_id] = ivf_index
        
        stats["ivf_index"] = ivf_index.get_stats()
        
        return stats
    
    async def _build_flat_index(self, library_id: UUID) -> Dict[str, Any]:
        """
        Build only the Flat index for a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            Dictionary with build statistics for flat index
        """
        # Get all chunks with embeddings
        chunks = await self.chunk_service.get_chunks_with_embeddings(library_id)
        
        if not chunks:
            return {
                "message": "No chunks with embeddings found",
                "flat_index": None
            }
        
        # Build Flat Index
        flat_index = FlatIndex(settings.embedding_dimension)
        flat_index.add_vectors(chunks)
        flat_index.build()
        self.flat_indexes[library_id] = flat_index
        
        return {
            "flat_index": flat_index.get_stats()
        }
    
    async def _build_ivf_index(self, library_id: UUID) -> Dict[str, Any]:
        """
        Build only the IVF index for a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            Dictionary with build statistics for IVF index
        """
        # Get all chunks with embeddings
        chunks = await self.chunk_service.get_chunks_with_embeddings(library_id)
        
        if not chunks:
            return {
                "message": "No chunks with embeddings found",
                "ivf_index": None
            }
        
        # Build IVF Index
        ivf_index = IVFIndex(settings.embedding_dimension)
        ivf_index.add_vectors(chunks)
        ivf_index.build()
        self.ivf_indexes[library_id] = ivf_index
        
        return {
            "ivf_index": ivf_index.get_stats()
        }
    
    async def search(self, library_id: UUID, search_query: SearchQuery, index_type: str = "flat") -> SearchResponse:
        """
        Perform k-NN search on a library.
        
        Args:
            library_id: Library ID
            search_query: Search query parameters
            index_type: Type of index to use ("flat" or "ivf")
            
        Returns:
            Search response with results
            
        Raises:
            ValueError: If library not found or index not built
        """
        start_time = time.time()
        
        # Generate query embedding
        query_embedding = embedding_service.get_query_embedding(search_query.query_text)
        
        # Get the appropriate index
        if index_type == "flat":
            index = self.flat_indexes.get(library_id)
            if not index:
                raise ValueError(f"Flat index not built for library {library_id}")
        elif index_type == "ivf":
            index = self.ivf_indexes.get(library_id)
            if not index:
                raise ValueError(f"IVF index not built for library {library_id}")
        else:
            raise ValueError(f"Invalid index type: {index_type}")
        
        # Perform search
        results = index.search(
            query_vector=query_embedding,
            k=search_query.k,
            metadata_filter=search_query.metadata_filter
        )
        
        # Convert to SearchResult objects
        search_results = []
        for rank, (chunk, similarity_score) in enumerate(results, 1):
            search_results.append(SearchResult(
                chunk=chunk,
                similarity_score=similarity_score,
                rank=rank
            ))
        
        search_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        return SearchResponse(
            query=search_query.query_text,
            results=search_results,
            total_results=len(search_results),
            search_time_ms=search_time
        )
    
    async def get_index_stats(self, library_id: UUID) -> Dict[str, Any]:
        """
        Get statistics for both indexes of a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            Dictionary with index statistics
        """
        stats = {}
        
        if library_id in self.flat_indexes:
            stats["flat_index"] = self.flat_indexes[library_id].get_stats()
        else:
            stats["flat_index"] = None
        
        if library_id in self.ivf_indexes:
            stats["ivf_index"] = self.ivf_indexes[library_id].get_stats()
        else:
            stats["ivf_index"] = None
        
        return stats
    
    async def clear_indexes(self, library_id: UUID) -> None:
        """
        Clear indexes for a library.
        
        Args:
            library_id: Library ID
        """
        if library_id in self.flat_indexes:
            self.flat_indexes[library_id].clear()
            del self.flat_indexes[library_id]
        
        if library_id in self.ivf_indexes:
            self.ivf_indexes[library_id].clear()
            del self.ivf_indexes[library_id]
    
    async def rebuild_indexes(self, library_id: UUID) -> Dict[str, Any]:
        """
        Rebuild indexes for a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            Dictionary with build statistics
        """
        # Clear existing indexes
        await self.clear_indexes(library_id)
        
        # Build new indexes
        return await self.build_indexes(library_id)
    
    def get_available_indexes(self, library_id: UUID) -> List[str]:
        """
        Get list of available indexes for a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            List of available index types
        """
        available = []
        if library_id in self.flat_indexes:
            available.append("flat")
        if library_id in self.ivf_indexes:
            available.append("ivf")
        return available
    
    async def build_flat_index(self, library_id: UUID) -> dict:
        """
        Build only the flat index for a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            Build statistics for flat index
        """
        return await self._build_flat_index(library_id)
    
    async def build_ivf_index(self, library_id: UUID) -> dict:
        """
        Build only the IVF index for a library.
        
        Args:
            library_id: Library ID
            
        Returns:
            Build statistics for IVF index
        """
        return await self._build_ivf_index(library_id)
