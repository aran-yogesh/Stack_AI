"""Base indexing interface and implementations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

import numpy as np

from app.models import Chunk


class BaseIndex(ABC):
    """Abstract base class for vector indexing algorithms."""
    
    def __init__(self, dimension: int):
        """
        Initialize the index.
        
        Args:
            dimension: Dimension of the embedding vectors
        """
        self.dimension = dimension
        self.is_built = False
    
    @abstractmethod
    def add_vectors(self, chunks: List[Chunk]) -> None:
        """
        Add vectors to the index.
        
        Args:
            chunks: List of chunks with embeddings to add
        """
        pass
    
    @abstractmethod
    def search(self, query_vector: List[float], k: int, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Tuple[Chunk, float]]:
        """
        Search for similar vectors.
        
        Args:
            query_vector: Query vector to search for
            k: Number of results to return
            metadata_filter: Optional metadata filter
            
        Returns:
            List of (chunk, similarity_score) tuples
        """
        pass
    
    @abstractmethod
    def build(self) -> None:
        """Build/finalize the index."""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        pass


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        a: First vector
        b: Second vector
        
    Returns:
        Cosine similarity score between 0 and 1
    """
    # Normalize vectors
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    # Calculate cosine similarity
    similarity = np.dot(a, b) / (norm_a * norm_b)
    return float(similarity)


def apply_metadata_filter(chunks: List[Chunk], metadata_filter: Dict[str, Any]) -> List[Chunk]:
    """
    Apply metadata filter to chunks.
    
    Args:
        chunks: List of chunks to filter
        metadata_filter: Filter criteria
        
    Returns:
        Filtered list of chunks
    """
    if not metadata_filter:
        return chunks
    
    filtered_chunks = []
    for chunk in chunks:
        match = True
        for key, value in metadata_filter.items():
            if key not in chunk.metadata or chunk.metadata[key] != value:
                match = False
                break
        if match:
            filtered_chunks.append(chunk)
    
    return filtered_chunks
