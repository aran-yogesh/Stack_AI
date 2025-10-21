"""Unit tests for indexing algorithms."""

from uuid import uuid4

import numpy as np
import pytest

from app.indexing.flat_index import FlatIndex
from app.indexing.ivf_index import IVFIndex
from app.models import Chunk


class TestFlatIndex:
    """Test cases for FlatIndex."""
    
    def setup_method(self):
        """Set up test data."""
        self.dimension = 3
        self.index = FlatIndex(self.dimension)
        
        # Create test chunks with embeddings
        self.chunks = [
            Chunk(
                id=uuid4(),
                document_id=uuid4(),
                text="First chunk",
                embedding=[1.0, 0.0, 0.0],
                metadata={"type": "test"}
            ),
            Chunk(
                id=uuid4(),
                document_id=uuid4(),
                text="Second chunk",
                embedding=[0.0, 1.0, 0.0],
                metadata={"type": "test"}
            ),
            Chunk(
                id=uuid4(),
                document_id=uuid4(),
                text="Third chunk",
                embedding=[0.0, 0.0, 1.0],
                metadata={"type": "other"}
            )
        ]
    
    def test_add_vectors(self):
        """Test adding vectors to index."""
        self.index.add_vectors(self.chunks)
        assert len(self.index.chunks) == 3
        assert self.index.vectors is None  # Not built yet
    
    def test_build_index(self):
        """Test building the index."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        assert self.index.is_built
        assert self.index.vectors is not None
        assert self.index.vectors.shape == (3, 3)
        assert self.index.build_time > 0
    
    def test_search_exact_match(self):
        """Test search with exact match."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        # Search for exact match
        query_vector = [1.0, 0.0, 0.0]
        results = self.index.search(query_vector, k=1)
        
        assert len(results) == 1
        chunk, similarity = results[0]
        assert chunk.text == "First chunk"
        assert similarity == 1.0
    
    def test_search_top_k(self):
        """Test search returning top k results."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        # Search for vector similar to first chunk
        query_vector = [0.9, 0.1, 0.0]
        results = self.index.search(query_vector, k=2)
        
        assert len(results) == 2
        # First result should be most similar
        assert results[0][1] >= results[1][1]
    
    def test_search_with_metadata_filter(self):
        """Test search with metadata filter."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        # Search with metadata filter
        query_vector = [0.0, 0.0, 1.0]
        metadata_filter = {"type": "test"}
        results = self.index.search(query_vector, k=10, metadata_filter=metadata_filter)
        
        # Should only return chunks with type="test"
        assert len(results) == 2
        for chunk, _ in results:
            assert chunk.metadata["type"] == "test"
    
    def test_empty_search(self):
        """Test search on empty index."""
        self.index.build()
        results = self.index.search([1.0, 0.0, 0.0], k=5)
        assert len(results) == 0
    
    def test_get_stats(self):
        """Test getting index statistics."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        stats = self.index.get_stats()
        assert stats["index_type"] == "Flat"
        assert stats["dimension"] == 3
        assert stats["num_vectors"] == 3
        assert stats["is_built"] is True
        assert stats["build_time"] > 0
        assert stats["memory_usage_mb"] > 0
    
    def test_clear_index(self):
        """Test clearing the index."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        self.index.clear()
        assert len(self.index.chunks) == 0
        assert self.index.vectors is None
        assert not self.index.is_built


class TestIVFIndex:
    """Test cases for IVFIndex."""
    
    def setup_method(self):
        """Set up test data."""
        self.dimension = 3
        self.n_clusters = 2
        self.index = IVFIndex(self.dimension, n_clusters=self.n_clusters)
        
        # Create test chunks with embeddings
        self.chunks = [
            Chunk(
                id=uuid4(),
                document_id=uuid4(),
                text="First chunk",
                embedding=[1.0, 0.0, 0.0],
                metadata={"type": "test"}
            ),
            Chunk(
                id=uuid4(),
                document_id=uuid4(),
                text="Second chunk",
                embedding=[0.0, 1.0, 0.0],
                metadata={"type": "test"}
            ),
            Chunk(
                id=uuid4(),
                document_id=uuid4(),
                text="Third chunk",
                embedding=[0.0, 0.0, 1.0],
                metadata={"type": "other"}
            )
        ]
    
    def test_add_vectors(self):
        """Test adding vectors to index."""
        self.index.add_vectors(self.chunks)
        assert len(self.index.chunks) == 3
        assert self.index.vectors is None  # Not built yet
    
    def test_build_index(self):
        """Test building the index."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        assert self.index.is_built
        assert self.index.vectors is not None
        assert self.index.cluster_centroids is not None
        assert self.index.cluster_assignments is not None
        assert len(self.index.cluster_assignments) == 3
        assert self.index.build_time > 0
    
    def test_kmeans_clustering(self):
        """Test K-Means clustering."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        # Check that all vectors are assigned to clusters
        assert len(self.index.cluster_assignments) == 3
        for assignment in self.index.cluster_assignments:
            assert 0 <= assignment < self.n_clusters
        
        # Check cluster indices
        assert len(self.index.cluster_indices) <= self.n_clusters
        total_assigned = sum(len(indices) for indices in self.index.cluster_indices.values())
        assert total_assigned == 3
    
    def test_search_approximate(self):
        """Test approximate search."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        # Search for vector similar to first chunk
        query_vector = [0.9, 0.1, 0.0]
        results = self.index.search(query_vector, k=2)
        
        assert len(results) <= 2
        # Results should be sorted by similarity
        for i in range(len(results) - 1):
            assert results[i][1] >= results[i + 1][1]
    
    def test_search_with_metadata_filter(self):
        """Test search with metadata filter."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        # Search with metadata filter
        query_vector = [0.0, 0.0, 1.0]
        metadata_filter = {"type": "test"}
        results = self.index.search(query_vector, k=10, metadata_filter=metadata_filter)
        
        # Should only return chunks with type="test"
        for chunk, _ in results:
            assert chunk.metadata["type"] == "test"
    
    def test_empty_search(self):
        """Test search on empty index."""
        self.index.build()
        results = self.index.search([1.0, 0.0, 0.0], k=5)
        assert len(results) == 0
    
    def test_get_stats(self):
        """Test getting index statistics."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        stats = self.index.get_stats()
        assert stats["index_type"] == "IVF-Flat"
        assert stats["dimension"] == 3
        assert stats["dimension"] == 3
        assert stats["num_vectors"] == 3
        assert stats["n_clusters"] == 2
        assert stats["is_built"] is True
        assert stats["build_time"] > 0
        assert stats["memory_usage_mb"] > 0
        assert "cluster_distribution" in stats
    
    def test_clear_index(self):
        """Test clearing the index."""
        self.index.add_vectors(self.chunks)
        self.index.build()
        
        self.index.clear()
        assert len(self.index.chunks) == 0
        assert self.index.vectors is None
        assert self.index.cluster_centroids is None
        assert self.index.cluster_assignments is None
        assert len(self.index.cluster_indices) == 0
        assert not self.index.is_built


class TestIndexComparison:
    """Test cases comparing Flat and IVF indexes."""
    
    def setup_method(self):
        """Set up test data."""
        self.dimension = 3
        self.chunks = [
            Chunk(
                id=uuid4(),
                document_id=uuid4(),
                text=f"Chunk {i}",
                embedding=[float(i), float(i+1), float(i+2)],
                metadata={"index": i}
            )
            for i in range(10)
        ]
    
    def test_build_time_comparison(self):
        """Test that IVF takes longer to build than Flat."""
        flat_index = FlatIndex(self.dimension)
        ivf_index = IVFIndex(self.dimension, n_clusters=3)
        
        flat_index.add_vectors(self.chunks)
        ivf_index.add_vectors(self.chunks)
        
        flat_index.build()
        ivf_index.build()
        
        # IVF should take longer to build due to clustering
        assert ivf_index.build_time > flat_index.build_time
    
    def test_search_quality_comparison(self):
        """Test that Flat gives exact results while IVF gives approximate."""
        flat_index = FlatIndex(self.dimension)
        ivf_index = IVFIndex(self.dimension, n_clusters=3)
        
        flat_index.add_vectors(self.chunks)
        ivf_index.add_vectors(self.chunks)
        
        flat_index.build()
        ivf_index.build()
        
        query_vector = [0.0, 1.0, 2.0]
        
        flat_results = flat_index.search(query_vector, k=3)
        ivf_results = ivf_index.search(query_vector, k=3)
        
        # Flat should return exact results
        assert len(flat_results) == 3
        
        # IVF should return approximate results (may be fewer due to clustering)
        assert len(ivf_results) <= 3
        
        # Flat results should be perfectly sorted
        for i in range(len(flat_results) - 1):
            assert flat_results[i][1] >= flat_results[i + 1][1]
