"""IVF-Flat (Inverted File Index) implementation with K-Means clustering."""

import random
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from app.config import settings
from app.indexing.base_index import BaseIndex, apply_metadata_filter, cosine_similarity
from app.models import Chunk


class IVFIndex(BaseIndex):
    """
    IVF-Flat (Inverted File Index) implementation with K-Means clustering.
    
    This index uses K-Means clustering to partition vectors into clusters,
    then searches only in the most relevant clusters for approximate results.
    
    Time Complexity:
    - Build: O(n*log(n)) - K-Means clustering + vector assignment
    - Search: O(k + n/k) - Search only in relevant clusters
    
    Space Complexity: O(n*d + k*d) - Vectors + cluster centroids
    
    Use Case: Best for large datasets where approximate results are acceptable
    """
    
    def __init__(self, dimension: int, n_clusters: int = None, max_iterations: int = None):
        """
        Initialize the IVF index.
        
        Args:
            dimension: Dimension of the embedding vectors
            n_clusters: Number of clusters for K-Means
            max_iterations: Maximum iterations for K-Means
        """
        super().__init__(dimension)
        self.n_clusters = n_clusters or settings.ivf_n_clusters
        self.max_iterations = max_iterations or settings.ivf_max_iterations
        
        self.chunks: List[Chunk] = []
        self.vectors: np.ndarray = None
        self.cluster_centroids: np.ndarray = None
        self.cluster_assignments: List[int] = None
        self.cluster_indices: Dict[int, List[int]] = {}  # cluster_id -> list of vector indices
        
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
        """Build the index using K-Means clustering."""
        if not self.chunks:
            self.is_built = True
            return
        
        start_time = time.time()
        
        # Convert embeddings to numpy array
        embeddings = [chunk.embedding for chunk in self.chunks]
        self.vectors = np.array(embeddings, dtype=np.float32)
        
        # Perform K-Means clustering
        self._kmeans_clustering()
        
        # Build cluster index
        self._build_cluster_index()
        
        self.build_time = time.time() - start_time
        self.is_built = True
    
    def _kmeans_clustering(self) -> None:
        """Perform K-Means clustering on the vectors."""
        n_vectors = len(self.vectors)
        
        # Initialize centroids randomly
        self.cluster_centroids = np.random.rand(self.n_clusters, self.dimension).astype(np.float32)
        
        # Normalize centroids
        for i in range(self.n_clusters):
            norm = np.linalg.norm(self.cluster_centroids[i])
            if norm > 0:
                self.cluster_centroids[i] /= norm
        
        # Initialize cluster assignments
        self.cluster_assignments = [0] * n_vectors
        
        # K-Means iterations
        for iteration in range(self.max_iterations):
            # Assign vectors to closest centroids
            new_assignments = self._assign_to_clusters()
            
            # Check for convergence
            if new_assignments == self.cluster_assignments:
                break
            
            self.cluster_assignments = new_assignments
            
            # Update centroids
            self._update_centroids()
    
    def _assign_to_clusters(self) -> List[int]:
        """Assign vectors to closest centroids."""
        assignments = []
        
        for vector in self.vectors:
            best_cluster = 0
            best_similarity = -1
            
            for cluster_id in range(self.n_clusters):
                similarity = cosine_similarity(vector, self.cluster_centroids[cluster_id])
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_cluster = cluster_id
            
            assignments.append(best_cluster)
        
        return assignments
    
    def _update_centroids(self) -> None:
        """Update cluster centroids based on current assignments."""
        for cluster_id in range(self.n_clusters):
            # Find vectors assigned to this cluster
            cluster_vectors = []
            for i, assignment in enumerate(self.cluster_assignments):
                if assignment == cluster_id:
                    cluster_vectors.append(self.vectors[i])
            
            if cluster_vectors:
                # Calculate mean vector
                mean_vector = np.mean(cluster_vectors, axis=0)
                
                # Normalize
                norm = np.linalg.norm(mean_vector)
                if norm > 0:
                    self.cluster_centroids[cluster_id] = mean_vector / norm
                else:
                    # If mean is zero vector, keep current centroid
                    pass
    
    def _build_cluster_index(self) -> None:
        """Build index mapping clusters to vector indices."""
        self.cluster_indices = {}
        
        for i, cluster_id in enumerate(self.cluster_assignments):
            if cluster_id not in self.cluster_indices:
                self.cluster_indices[cluster_id] = []
            self.cluster_indices[cluster_id].append(i)
    
    def search(self, query_vector: List[float], k: int, metadata_filter: Optional[Dict[str, Any]] = None) -> List[Tuple[Chunk, float]]:
        """
        Search for similar vectors using IVF.
        
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
        
        # Find most similar clusters
        cluster_similarities = []
        for cluster_id in range(self.n_clusters):
            similarity = cosine_similarity(query_array, self.cluster_centroids[cluster_id])
            cluster_similarities.append((cluster_id, similarity))
        
        # Sort clusters by similarity (descending)
        cluster_similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Search in most relevant clusters
        similarities = []
        vectors_searched = 0
        
        # Search in top clusters until we have enough candidates
        for cluster_id, _ in cluster_similarities:
            if cluster_id in self.cluster_indices:
                cluster_vector_indices = self.cluster_indices[cluster_id]
                
                # Calculate similarities for vectors in this cluster
                for vector_idx in cluster_vector_indices:
                    chunk = self.chunks[vector_idx]
                    similarity = cosine_similarity(query_array, self.vectors[vector_idx])
                    similarities.append((chunk, similarity))
                    vectors_searched += 1
                
                # If we have enough candidates, break
                if len(similarities) >= k * 2:  # Search in more clusters for better recall
                    break
        
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
        
        # Calculate cluster distribution
        cluster_sizes = [len(indices) for indices in self.cluster_indices.values()]
        
        return {
            "index_type": "IVF-Flat",
            "dimension": self.dimension,
            "num_vectors": len(self.chunks),
            "n_clusters": self.n_clusters,
            "is_built": self.is_built,
            "build_time": self.build_time,
            "avg_search_time": avg_search_time,
            "total_searches": len(self.search_times),
            "memory_usage_mb": (
                (self.vectors.nbytes + self.cluster_centroids.nbytes) / (1024 * 1024)
                if self.vectors is not None else 0.0
            ),
            "cluster_distribution": {
                "min_size": min(cluster_sizes) if cluster_sizes else 0,
                "max_size": max(cluster_sizes) if cluster_sizes else 0,
                "avg_size": np.mean(cluster_sizes) if cluster_sizes else 0.0
            }
        }
    
    def clear(self) -> None:
        """Clear the index."""
        self.chunks.clear()
        self.vectors = None
        self.cluster_centroids = None
        self.cluster_assignments = None
        self.cluster_indices.clear()
        self.is_built = False
        self.build_time = 0.0
        self.search_times.clear()
