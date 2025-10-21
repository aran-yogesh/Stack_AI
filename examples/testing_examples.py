#!/usr/bin/env python3
"""
Comprehensive Testing Examples for Stack AI Vector Database

This script demonstrates various testing approaches including:
- Unit tests for individual components
- Integration tests for API endpoints
- Performance tests for load testing
- End-to-end tests for complete workflows

Usage:
    python examples/testing_examples.py
"""

import asyncio
import json
import time
from typing import Any, Dict, List
from uuid import UUID, uuid4

import httpx
import pytest

from app.models import ChunkCreate, DocumentCreate, LibraryCreate


class TestVectorDBAPI:
    """Comprehensive test suite for Vector Database API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_data = {}
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def setup_test_data(self):
        """Set up test data for testing."""
        print("🔧 Setting up test data...")
        
        # Create test library
        library_data = {
            "name": "Test Library",
            "description": "A library for testing purposes",
            "metadata": {"test": True, "version": "1.0"}
        }
        response = await self.client.post(f"{self.base_url}/libraries/", json=library_data)
        response.raise_for_status()
        self.test_data['library'] = response.json()
        
        # Create test document
        document_data = {
            "title": "Test Document",
            "content": "This is a test document for testing the vector database functionality.",
            "metadata": {"author": "Test Author", "category": "testing"}
        }
        response = await self.client.post(
            f"{self.base_url}/libraries/{self.test_data['library']['id']}/documents/",
            json=document_data
        )
        response.raise_for_status()
        self.test_data['document'] = response.json()
        
        # Create test chunks
        chunks_data = [
            {
                "text": "Machine learning is a subset of artificial intelligence.",
                "metadata": {"section": "introduction", "topic": "ml"}
            },
            {
                "text": "Deep learning uses neural networks with multiple layers.",
                "metadata": {"section": "deep_learning", "topic": "neural_networks"}
            },
            {
                "text": "Natural language processing deals with text and speech data.",
                "metadata": {"section": "nlp", "topic": "text_processing"}
            }
        ]
        
        self.test_data['chunks'] = []
        for chunk_data in chunks_data:
            response = await self.client.post(
                f"{self.base_url}/libraries/{self.test_data['library']['id']}/documents/{self.test_data['document']['id']}/chunks/",
                json=chunk_data
            )
            response.raise_for_status()
            self.test_data['chunks'].append(response.json())
        
        print(f"✅ Created test library: {self.test_data['library']['name']}")
        print(f"✅ Created test document: {self.test_data['document']['title']}")
        print(f"✅ Created {len(self.test_data['chunks'])} test chunks")
    
    async def cleanup_test_data(self):
        """Clean up test data."""
        print("🧹 Cleaning up test data...")
        
        if 'library' in self.test_data:
            try:
                await self.client.delete(f"{self.base_url}/libraries/{self.test_data['library']['id']}")
                print("✅ Test data cleaned up")
            except Exception as e:
                print(f"⚠️  Warning: Could not clean up test data: {e}")
    
    # Unit Tests
    async def test_api_health(self):
        """Test API health endpoint."""
        print("\n🏥 Testing API Health...")
        
        response = await self.client.get(f"{self.base_url}/health")
        assert response.status_code == 200
        
        health_data = response.json()
        assert health_data['status'] == 'healthy'
        assert 'message' in health_data
        
        print("✅ API health check passed")
    
    async def test_root_endpoint(self):
        """Test root endpoint."""
        print("\n🏠 Testing Root Endpoint...")
        
        response = await self.client.get(f"{self.base_url}/")
        assert response.status_code == 200
        
        root_data = response.json()
        assert 'message' in root_data
        assert 'version' in root_data
        assert 'endpoints' in root_data
        
        print("✅ Root endpoint test passed")
    
    # Library Tests
    async def test_library_crud(self):
        """Test complete Library CRUD operations."""
        print("\n🏛️  Testing Library CRUD...")
        
        # Create
        library_data = {
            "name": "Test Library CRUD",
            "description": "Testing library operations",
            "metadata": {"test": "crud"}
        }
        response = await self.client.post(f"{self.base_url}/libraries/", json=library_data)
        assert response.status_code == 201
        
        library = response.json()
        assert library['name'] == library_data['name']
        assert library['description'] == library_data['description']
        assert library['metadata'] == library_data['metadata']
        assert 'id' in library
        assert 'created_at' in library
        assert 'updated_at' in library
        
        library_id = library['id']
        
        # Read
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}")
        assert response.status_code == 200
        
        retrieved_library = response.json()
        assert retrieved_library['id'] == library_id
        assert retrieved_library['name'] == library_data['name']
        
        # Update
        update_data = {
            "name": "Updated Test Library",
            "description": "Updated description",
            "metadata": {"test": "crud", "updated": True}
        }
        response = await self.client.put(f"{self.base_url}/libraries/{library_id}", json=update_data)
        assert response.status_code == 200
        
        updated_library = response.json()
        assert updated_library['name'] == update_data['name']
        assert updated_library['description'] == update_data['description']
        assert updated_library['metadata']['updated'] == True
        
        # Delete
        response = await self.client.delete(f"{self.base_url}/libraries/{library_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}")
        assert response.status_code == 404
        
        print("✅ Library CRUD tests passed")
    
    async def test_library_validation(self):
        """Test library validation."""
        print("\n🔍 Testing Library Validation...")
        
        # Test empty name
        response = await self.client.post(f"{self.base_url}/libraries/", json={"name": ""})
        assert response.status_code == 422
        
        # Test missing name
        response = await self.client.post(f"{self.base_url}/libraries/", json={})
        assert response.status_code == 422
        
        # Test long name
        long_name = "x" * 101  # Exceeds max_length=100
        response = await self.client.post(f"{self.base_url}/libraries/", json={"name": long_name})
        assert response.status_code == 422
        
        print("✅ Library validation tests passed")
    
    # Document Tests
    async def test_document_crud(self):
        """Test complete Document CRUD operations."""
        print("\n📄 Testing Document CRUD...")
        
        library_id = self.test_data['library']['id']
        
        # Create
        document_data = {
            "title": "Test Document CRUD",
            "content": "Testing document operations",
            "metadata": {"test": "crud", "author": "Test Author"}
        }
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/documents/", json=document_data)
        assert response.status_code == 201
        
        document = response.json()
        assert document['title'] == document_data['title']
        assert document['content'] == document_data['content']
        assert document['metadata'] == document_data['metadata']
        assert document['library_id'] == library_id
        assert 'id' in document
        
        document_id = document['id']
        
        # Read
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/{document_id}")
        assert response.status_code == 200
        
        retrieved_document = response.json()
        assert retrieved_document['id'] == document_id
        assert retrieved_document['title'] == document_data['title']
        
        # Update
        update_data = {
            "title": "Updated Test Document",
            "content": "Updated content",
            "metadata": {"test": "crud", "author": "Test Author", "updated": True}
        }
        response = await self.client.put(f"{self.base_url}/libraries/{library_id}/documents/{document_id}", json=update_data)
        assert response.status_code == 200
        
        updated_document = response.json()
        assert updated_document['title'] == update_data['title']
        assert updated_document['content'] == update_data['content']
        assert updated_document['metadata']['updated'] == True
        
        # Delete
        response = await self.client.delete(f"{self.base_url}/libraries/{library_id}/documents/{document_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/{document_id}")
        assert response.status_code == 404
        
        print("✅ Document CRUD tests passed")
    
    # Chunk Tests
    async def test_chunk_crud(self):
        """Test complete Chunk CRUD operations."""
        print("\n🧩 Testing Chunk CRUD...")
        
        library_id = self.test_data['library']['id']
        document_id = self.test_data['document']['id']
        
        # Create
        chunk_data = {
            "text": "This is a test chunk for CRUD operations.",
            "metadata": {"test": "crud", "section": "testing"}
        }
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/", json=chunk_data)
        assert response.status_code == 201
        
        chunk = response.json()
        assert chunk['text'] == chunk_data['text']
        assert chunk['metadata'] == chunk_data['metadata']
        assert chunk['document_id'] == document_id
        assert 'id' in chunk
        
        chunk_id = chunk['id']
        
        # Read
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}")
        assert response.status_code == 200
        
        retrieved_chunk = response.json()
        assert retrieved_chunk['id'] == chunk_id
        assert retrieved_chunk['text'] == chunk_data['text']
        
        # Update
        update_data = {
            "text": "Updated test chunk for CRUD operations.",
            "metadata": {"test": "crud", "section": "testing", "updated": True}
        }
        response = await self.client.put(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}", json=update_data)
        assert response.status_code == 200
        
        updated_chunk = response.json()
        assert updated_chunk['text'] == update_data['text']
        assert updated_chunk['metadata']['updated'] == True
        
        # Delete
        response = await self.client.delete(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}")
        assert response.status_code == 404
        
        print("✅ Chunk CRUD tests passed")
    
    # Search Tests
    async def test_search_operations(self):
        """Test search operations."""
        print("\n🔍 Testing Search Operations...")
        
        library_id = self.test_data['library']['id']
        
        # Build index
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/index")
        assert response.status_code == 200
        
        # Wait for indexing to complete
        await asyncio.sleep(2)
        
        # Test search
        search_data = {
            "query_text": "machine learning",
            "k": 5
        }
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/search", json=search_data)
        assert response.status_code == 200
        
        search_results = response.json()
        assert 'query' in search_results
        assert 'results' in search_results
        assert 'total_results' in search_results
        assert 'search_time_ms' in search_results
        assert isinstance(search_results['results'], list)
        
        # Test search with metadata filter
        filtered_search_data = {
            "query_text": "learning",
            "k": 3,
            "metadata_filter": {"topic": "ml"}
        }
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/search", json=filtered_search_data)
        assert response.status_code == 200
        
        filtered_results = response.json()
        assert 'results' in filtered_results
        
        print("✅ Search operation tests passed")
    
    # Integration Tests
    async def test_cascade_deletion(self):
        """Test cascade deletion operations."""
        print("\n🗑️  Testing Cascade Deletion...")
        
        library_id = self.test_data['library']['id']
        document_id = self.test_data['document']['id']
        
        # Verify chunks exist
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/")
        assert response.status_code == 200
        chunks = response.json()
        assert len(chunks) > 0
        
        # Delete document
        response = await self.client.delete(f"{self.base_url}/libraries/{library_id}/documents/{document_id}")
        assert response.status_code == 204
        
        # Verify chunks are deleted
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/")
        assert response.status_code == 404
        
        print("✅ Cascade deletion tests passed")
    
    async def test_data_consistency(self):
        """Test data consistency across operations."""
        print("\n🔄 Testing Data Consistency...")
        
        library_id = self.test_data['library']['id']
        
        # Get library with documents
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}")
        assert response.status_code == 200
        
        library = response.json()
        assert 'documents' in library
        assert isinstance(library['documents'], list)
        
        # Verify document count matches
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/")
        assert response.status_code == 200
        
        documents = response.json()
        assert len(documents) == len(library['documents'])
        
        print("✅ Data consistency tests passed")
    
    # Performance Tests
    async def test_concurrent_operations(self):
        """Test concurrent operations."""
        print("\n⚡ Testing Concurrent Operations...")
        
        library_id = self.test_data['library']['id']
        document_id = self.test_data['document']['id']
        
        # Create multiple chunks concurrently
        chunk_tasks = []
        for i in range(10):
            chunk_data = {
                "text": f"Concurrent test chunk {i}",
                "metadata": {"test": "concurrent", "index": i}
            }
            task = self.client.post(
                f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/",
                json=chunk_data
            )
            chunk_tasks.append(task)
        
        start_time = time.time()
        responses = await asyncio.gather(*chunk_tasks)
        end_time = time.time()
        
        # Verify all chunks were created successfully
        for response in responses:
            assert response.status_code == 201
        
        print(f"✅ Created 10 chunks concurrently in {end_time - start_time:.2f} seconds")
        
        # Test concurrent searches
        search_tasks = []
        for i in range(5):
            search_data = {
                "query_text": f"test chunk {i}",
                "k": 3
            }
            task = self.client.post(f"{self.base_url}/libraries/{library_id}/search", json=search_data)
            search_tasks.append(task)
        
        start_time = time.time()
        search_responses = await asyncio.gather(*search_tasks)
        end_time = time.time()
        
        # Verify all searches completed successfully
        for response in search_responses:
            assert response.status_code == 200
        
        print(f"✅ Performed 5 concurrent searches in {end_time - start_time:.2f} seconds")
    
    async def test_large_dataset(self):
        """Test with larger dataset."""
        print("\n📊 Testing Large Dataset...")
        
        library_id = self.test_data['library']['id']
        document_id = self.test_data['document']['id']
        
        # Create many chunks
        chunk_count = 100
        print(f"Creating {chunk_count} chunks...")
        
        start_time = time.time()
        for i in range(chunk_count):
            chunk_data = {
                "text": f"Large dataset test chunk {i} with some content about machine learning and artificial intelligence.",
                "metadata": {"test": "large_dataset", "index": i, "category": "test"}
            }
            response = await self.client.post(
                f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/",
                json=chunk_data
            )
            assert response.status_code == 201
        
        creation_time = time.time() - start_time
        print(f"✅ Created {chunk_count} chunks in {creation_time:.2f} seconds")
        
        # Build index
        print("Building search index...")
        start_time = time.time()
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/index")
        assert response.status_code == 200
        index_time = time.time() - start_time
        print(f"✅ Built index in {index_time:.2f} seconds")
        
        # Test search performance
        print("Testing search performance...")
        search_queries = [
            "machine learning",
            "artificial intelligence",
            "test chunk",
            "large dataset",
            "content about"
        ]
        
        total_search_time = 0
        for query in search_queries:
            start_time = time.time()
            search_data = {
                "query_text": query,
                "k": 10
            }
            response = await self.client.post(f"{self.base_url}/libraries/{library_id}/search", json=search_data)
            assert response.status_code == 200
            search_time = time.time() - start_time
            total_search_time += search_time
            
            results = response.json()
            print(f"   Query '{query}': {results['total_results']} results in {search_time:.3f}s")
        
        avg_search_time = total_search_time / len(search_queries)
        print(f"✅ Average search time: {avg_search_time:.3f} seconds")
    
    # Error Handling Tests
    async def test_error_handling(self):
        """Test error handling."""
        print("\n⚠️  Testing Error Handling...")
        
        # Test 404 errors
        fake_id = "00000000-0000-0000-0000-000000000000"
        
        response = await self.client.get(f"{self.base_url}/libraries/{fake_id}")
        assert response.status_code == 404
        
        response = await self.client.get(f"{self.base_url}/libraries/{fake_id}/documents/{fake_id}")
        assert response.status_code == 404
        
        response = await self.client.get(f"{self.base_url}/libraries/{fake_id}/documents/{fake_id}/chunks/{fake_id}")
        assert response.status_code == 404
        
        # Test validation errors
        response = await self.client.post(f"{self.base_url}/libraries/", json={"name": ""})
        assert response.status_code == 422
        
        response = await self.client.post(f"{self.base_url}/libraries/", json={"name": "x" * 101})
        assert response.status_code == 422
        
        print("✅ Error handling tests passed")
    
    # Export Tests
    async def test_export_operations(self):
        """Test export operations."""
        print("\n📤 Testing Export Operations...")
        
        # Test CSV export
        response = await self.client.get(f"{self.base_url}/csv/export")
        assert response.status_code == 200
        
        csv_data = response.text
        assert len(csv_data) > 0
        assert "library_id" in csv_data
        assert "document_id" in csv_data
        assert "chunk_id" in csv_data
        
        print("✅ Export operations tests passed")
    
    async def run_all_tests(self):
        """Run all tests."""
        print("🧪 Running Comprehensive Test Suite")
        print("=" * 60)
        
        try:
            await self.setup_test_data()
            
            # Unit Tests
            await self.test_api_health()
            await self.test_root_endpoint()
            
            # CRUD Tests
            await self.test_library_crud()
            await self.test_library_validation()
            await self.test_document_crud()
            await self.test_chunk_crud()
            
            # Search Tests
            await self.test_search_operations()
            
            # Integration Tests
            await self.test_cascade_deletion()
            await self.test_data_consistency()
            
            # Performance Tests
            await self.test_concurrent_operations()
            await self.test_large_dataset()
            
            # Error Handling Tests
            await self.test_error_handling()
            
            # Export Tests
            await self.test_export_operations()
            
            print("\n🎉 All tests passed successfully!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            await self.cleanup_test_data()
            await self.close()


async def run_performance_benchmark():
    """Run performance benchmark tests."""
    print("\n🚀 Performance Benchmark")
    print("=" * 60)
    
    client = httpx.AsyncClient(timeout=60.0)
    
    try:
        # Create test library
        library_data = {
            "name": "Performance Test Library",
            "description": "Library for performance testing",
            "metadata": {"test": "performance"}
        }
        response = await client.post("http://localhost:8000/libraries/", json=library_data)
        response.raise_for_status()
        library = response.json()
        library_id = library['id']
        
        # Create test document
        document_data = {
            "title": "Performance Test Document",
            "content": "Document for performance testing",
            "metadata": {"test": "performance"}
        }
        response = await client.post(f"http://localhost:8000/libraries/{library_id}/documents/", json=document_data)
        response.raise_for_status()
        document = response.json()
        document_id = document['id']
        
        # Benchmark chunk creation
        print("📊 Benchmarking chunk creation...")
        chunk_count = 1000
        start_time = time.time()
        
        for i in range(chunk_count):
            chunk_data = {
                "text": f"Performance test chunk {i} with some content about machine learning, artificial intelligence, and data science.",
                "metadata": {"test": "performance", "index": i, "category": "benchmark"}
            }
            response = await client.post(
                f"http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/",
                json=chunk_data
            )
            response.raise_for_status()
        
        creation_time = time.time() - start_time
        chunks_per_second = chunk_count / creation_time
        print(f"✅ Created {chunk_count} chunks in {creation_time:.2f} seconds")
        print(f"📈 Rate: {chunks_per_second:.2f} chunks/second")
        
        # Benchmark index building
        print("\n📊 Benchmarking index building...")
        start_time = time.time()
        response = await client.post(f"http://localhost:8000/libraries/{library_id}/index")
        response.raise_for_status()
        index_time = time.time() - start_time
        print(f"✅ Built index in {index_time:.2f} seconds")
        
        # Benchmark search performance
        print("\n📊 Benchmarking search performance...")
        search_queries = [
            "machine learning",
            "artificial intelligence",
            "data science",
            "neural networks",
            "deep learning",
            "natural language processing",
            "computer vision",
            "reinforcement learning",
            "supervised learning",
            "unsupervised learning"
        ]
        
        total_search_time = 0
        total_results = 0
        
        for query in search_queries:
            start_time = time.time()
            search_data = {
                "query_text": query,
                "k": 20
            }
            response = await client.post(f"http://localhost:8000/libraries/{library_id}/search", json=search_data)
            response.raise_for_status()
            search_time = time.time() - start_time
            total_search_time += search_time
            
            results = response.json()
            total_results += results['total_results']
            print(f"   Query '{query}': {results['total_results']} results in {search_time:.3f}s")
        
        avg_search_time = total_search_time / len(search_queries)
        avg_results_per_query = total_results / len(search_queries)
        print(f"\n📈 Average search time: {avg_search_time:.3f} seconds")
        print(f"📈 Average results per query: {avg_results_per_query:.1f}")
        
        # Cleanup
        await client.delete(f"http://localhost:8000/libraries/{library_id}")
        print("\n✅ Performance benchmark completed")
        
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await client.aclose()


async def main():
    """Main function to run all tests."""
    print("🧪 Stack AI Vector Database - Testing Examples")
    print("=" * 60)
    
    # Check if API is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code != 200:
                raise Exception("API not healthy")
    except Exception as e:
        print(f"❌ API not available: {e}")
        print("Please start the API server first: python -m uvicorn app.main:app --reload")
        return
    
    # Run comprehensive tests
    test_suite = TestVectorDBAPI()
    await test_suite.run_all_tests()
    
    # Run performance benchmark
    await run_performance_benchmark()


if __name__ == "__main__":
    asyncio.run(main())
