"""Flat (Brute Force) indexing implementation."""

import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from app.indexing.base_index import BaseIndex, apply_metadata_filter, cosine_similarity
from app.models import Chunk


class FlatIndex(BaseIndex):
    """
    Flat (Brute Force) index implementation.
    
    This index performs exact cosine similarity search by comparing
    the query vector with all stored vectors.
    
    Time Complexity:
    - Build: O(n) - Linear scan to store vectors
    - Search: O(n) - Brute force comparison with all vectors
    
    Space Complexity: O(n*d) - Stores all vectors in memory
    
    Use Case: Best for small datasets or when exact results are required
    """
    
    def __init__(self, dimension: int):
        """
        Initialize the flat index.
        
        Args:
            dimension: Dimension of the embedding vectors
        """
        super().__init__(dimension)
        self.chunks: List[Chunk] = []
        self.vectors: np.ndarray = None
        self.build_time: float = 0.0
        self.search_times: List[float] = []
    
    def add_vectors(self, chunks: List[Chunk]) -> None:
        """
        Add vectors to the index.
        
        Args:
            chunks: List of chunks with embeddings to add
        """
        if not chunks:
            return
        
        # Validate embeddings
        valid_chunks = []
        for chunk in chunks:
            if chunk.embedding is not None and len(chunk.embedding) == self.dimension:
                valid_chunks.append(chunk)
            else:
                raise ValueError(f"Invalid embedding for chunk {chunk.id}")
        
        self.chunks.extend(valid_chunks)
    
    def build(self) -> None:
        """Build the index by converting embeddings to numpy array."""
        if not self.chunks:
            self.is_built = True
            return
        
        start_time = time.time()
        
        # Convert embeddings to numpy array for efficient computation
        embeddings = [chunk.embedding for chunk in self.chunks]
        self.vectors = np.array(embeddings, dtype=np.float32)
        
        self.build_time = time.time() - start_time
        self.is_built = True
    
    def search(self, query_vector: List[float], k: int, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Tuple[Chunk, float]]:
        """
        Search for similar vectors using brute force.
        
        Args:
            query_vector: Query vector to search for
            k: Number of results to return
            metadata_filter: Optional metadata filter
            
        Returns:
            List of (chunk, similarity_score) tuples sorted by similarity
        """
        if not self.is_built:
            raise RuntimeError("Index must be built before searching")
        
        if not self.chunks:
            return []
        
        start_time = time.time()
        
        # Convert query to numpy array
        query_array = np.array(query_vector, dtype=np.float32)
        
        # Calculate cosine similarities
        similarities = []
        for i, chunk in enumerate(self.chunks):
            similarity = cosine_similarity(query_array, self.vectors[i])
            similarities.append((chunk, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Apply metadata filter if provided
        if metadata_filter:
            filtered_similarities = []
            for chunk, similarity in similarities:
                if self._chunk_matches_filter(chunk, metadata_filter):
                    filtered_similarities.append((chunk, similarity))
            similarities = filtered_similarities
        
        # Take top k results
        results = similarities[:k]
        
        # Record search time
        search_time = time.time() - start_time
        self.search_times.append(search_time)
        
        return results
    
    def _chunk_matches_filter(self, chunk: Chunk, metadata_filter: Dict[str, Any]) -> bool:
        """
        Check if a chunk matches the metadata filter.
        
        Args:
            chunk: Chunk to check
            metadata_filter: Filter criteria
            
        Returns:
            True if chunk matches filter, False otherwise
        """
        for key, value in metadata_filter.items():
            if key not in chunk.metadata or chunk.metadata[key] != value:
                return False
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get index statistics.
        
        Returns:
            Dictionary containing index statistics
        """
        avg_search_time = np.mean(self.search_times) if self.search_times else 0.0
        
        return {
            "index_type": "Flat",
            "dimension": self.dimension,
            "num_vectors": len(self.chunks),
            "is_built": self.is_built,
            "build_time": self.build_time,
            "avg_search_time": avg_search_time,
            "total_searches": len(self.search_times),
            "memory_usage_mb": (self.vectors.nbytes / (1024 * 1024)) if self.vectors is not None else 0.0
        }
    
    def clear(self) -> None:
        """Clear the index."""
        self.chunks.clear()
        self.vectors = None
        self.is_built = False
        self.build_time = 0.0
        self.search_times.clear()
