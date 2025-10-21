#!/usr/bin/env python3
"""
Comprehensive CRUD Examples for Stack AI Vector Database

This script demonstrates all CRUD operations for Libraries, Documents, and Chunks
with practical examples that can be easily implemented and tested.

Usage:
    python examples/crud_examples.py
"""

import asyncio
import json
import time
from typing import Any, Dict, List
from uuid import UUID

import httpx

from app.models import (
    ChunkCreate,
    ChunkUpdate,
    DocumentCreate,
    DocumentUpdate,
    LibraryCreate,
    LibraryUpdate,
    SearchQuery,
)


class VectorDBClient:
    """Client for interacting with the Vector Database API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    # Library CRUD Operations
    async def create_library(self, name: str, description: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new library."""
        data = {
            "name": name,
            "description": description,
            "metadata": metadata or {}
        }
        response = await self.client.post(f"{self.base_url}/libraries/", json=data)
        response.raise_for_status()
        return response.json()
    
    async def get_library(self, library_id: UUID) -> Dict[str, Any]:
        """Get a library by ID."""
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}")
        response.raise_for_status()
        return response.json()
    
    async def get_all_libraries(self) -> List[Dict[str, Any]]:
        """Get all libraries."""
        response = await self.client.get(f"{self.base_url}/libraries/")
        response.raise_for_status()
        return response.json()
    
    async def update_library(self, library_id: UUID, name: str = None, description: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Update a library."""
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if metadata is not None:
            data["metadata"] = metadata
        
        response = await self.client.put(f"{self.base_url}/libraries/{library_id}", json=data)
        response.raise_for_status()
        return response.json()
    
    async def delete_library(self, library_id: UUID) -> bool:
        """Delete a library."""
        response = await self.client.delete(f"{self.base_url}/libraries/{library_id}")
        response.raise_for_status()
        return response.status_code == 204
    
    # Document CRUD Operations
    async def create_document(self, library_id: UUID, title: str, content: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new document."""
        data = {
            "title": title,
            "content": content,
            "metadata": metadata or {}
        }
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/documents/", json=data)
        response.raise_for_status()
        return response.json()
    
    async def get_document(self, library_id: UUID, document_id: UUID) -> Dict[str, Any]:
        """Get a document by ID."""
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/{document_id}")
        response.raise_for_status()
        return response.json()
    
    async def get_documents(self, library_id: UUID) -> List[Dict[str, Any]]:
        """Get all documents in a library."""
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/")
        response.raise_for_status()
        return response.json()
    
    async def update_document(self, library_id: UUID, document_id: UUID, title: str = None, content: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Update a document."""
        data = {}
        if title is not None:
            data["title"] = title
        if content is not None:
            data["content"] = content
        if metadata is not None:
            data["metadata"] = metadata
        
        response = await self.client.put(f"{self.base_url}/libraries/{library_id}/documents/{document_id}", json=data)
        response.raise_for_status()
        return response.json()
    
    async def delete_document(self, library_id: UUID, document_id: UUID) -> bool:
        """Delete a document."""
        response = await self.client.delete(f"{self.base_url}/libraries/{library_id}/documents/{document_id}")
        response.raise_for_status()
        return response.status_code == 204
    
    # Chunk CRUD Operations
    async def create_chunk(self, library_id: UUID, document_id: UUID, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new chunk."""
        data = {
            "text": text,
            "metadata": metadata or {}
        }
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/", json=data)
        response.raise_for_status()
        return response.json()
    
    async def get_chunk(self, library_id: UUID, document_id: UUID, chunk_id: UUID) -> Dict[str, Any]:
        """Get a chunk by ID."""
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}")
        response.raise_for_status()
        return response.json()
    
    async def get_chunks(self, library_id: UUID, document_id: UUID) -> List[Dict[str, Any]]:
        """Get all chunks in a document."""
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/")
        response.raise_for_status()
        return response.json()
    
    async def update_chunk(self, library_id: UUID, document_id: UUID, chunk_id: UUID, text: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Update a chunk."""
        data = {}
        if text is not None:
            data["text"] = text
        if metadata is not None:
            data["metadata"] = metadata
        
        response = await self.client.put(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}", json=data)
        response.raise_for_status()
        return response.json()
    
    async def delete_chunk(self, library_id: UUID, document_id: UUID, chunk_id: UUID) -> bool:
        """Delete a chunk."""
        response = await self.client.delete(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}")
        response.raise_for_status()
        return response.status_code == 204
    
    # Search Operations
    async def build_index(self, library_id: UUID) -> Dict[str, Any]:
        """Build search index for a library."""
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/index")
        response.raise_for_status()
        return response.json()
    
    async def search(self, library_id: UUID, query_text: str, k: int = 10, metadata_filter: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search for similar chunks."""
        data = {
            "query_text": query_text,
            "k": k,
            "metadata_filter": metadata_filter
        }
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/search", json=data)
        response.raise_for_status()
        return response.json()
    
    # Utility Operations
    async def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        response = await self.client.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    async def export_csv(self) -> str:
        """Export all data to CSV."""
        response = await self.client.get(f"{self.base_url}/csv/export")
        response.raise_for_status()
        return response.text


async def demonstrate_library_crud():
    """Demonstrate Library CRUD operations."""
    print("🏛️  Library CRUD Operations")
    print("=" * 50)
    
    client = VectorDBClient()
    
    try:
        # Create libraries
        print("1. Creating libraries...")
        library1 = await client.create_library(
            name="Machine Learning Library",
            description="A collection of ML papers and resources",
            metadata={"category": "AI", "version": "1.0"}
        )
        print(f"   ✅ Created library: {library1['name']} (ID: {library1['id']})")
        
        library2 = await client.create_library(
            name="Python Documentation",
            description="Python programming guides and examples",
            metadata={"category": "Programming", "language": "Python"}
        )
        print(f"   ✅ Created library: {library2['name']} (ID: {library2['id']})")
        
        # Read libraries
        print("\n2. Reading libraries...")
        all_libraries = await client.get_all_libraries()
        print(f"   📚 Total libraries: {len(all_libraries)}")
        for lib in all_libraries:
            print(f"   - {lib['name']}: {lib['description']}")
        
        # Get specific library
        library1_details = await client.get_library(library1['id'])
        print(f"\n   📖 Library details: {library1_details['name']}")
        print(f"   📝 Description: {library1_details['description']}")
        print(f"   🏷️  Metadata: {library1_details['metadata']}")
        
        # Update library
        print("\n3. Updating library...")
        updated_library = await client.update_library(
            library1['id'],
            description="Updated: A comprehensive collection of ML papers and resources",
            metadata={"category": "AI", "version": "2.0", "updated": True}
        )
        print(f"   ✅ Updated library: {updated_library['name']}")
        print(f"   📝 New description: {updated_library['description']}")
        
        return library1['id'], library2['id']
        
    finally:
        await client.close()


async def demonstrate_document_crud(library_id: UUID):
    """Demonstrate Document CRUD operations."""
    print("\n📄 Document CRUD Operations")
    print("=" * 50)
    
    client = VectorDBClient()
    
    try:
        # Create documents
        print("1. Creating documents...")
        doc1 = await client.create_document(
            library_id=library_id,
            title="Introduction to Machine Learning",
            content="Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data.",
            metadata={"author": "John Doe", "pages": 50, "difficulty": "beginner"}
        )
        print(f"   ✅ Created document: {doc1['title']} (ID: {doc1['id']})")
        
        doc2 = await client.create_document(
            library_id=library_id,
            title="Deep Learning Fundamentals",
            content="Deep learning uses neural networks with multiple layers to model complex patterns in data.",
            metadata={"author": "Jane Smith", "pages": 100, "difficulty": "intermediate"}
        )
        print(f"   ✅ Created document: {doc2['title']} (ID: {doc2['id']})")
        
        # Read documents
        print("\n2. Reading documents...")
        all_docs = await client.get_documents(library_id)
        print(f"   📚 Total documents: {len(all_docs)}")
        for doc in all_docs:
            print(f"   - {doc['title']} by {doc['metadata'].get('author', 'Unknown')}")
        
        # Get specific document
        doc1_details = await client.get_document(library_id, doc1['id'])
        print(f"\n   📖 Document details: {doc1_details['title']}")
        print(f"   📝 Content: {doc1_details['content'][:100]}...")
        print(f"   🏷️  Metadata: {doc1_details['metadata']}")
        
        # Update document
        print("\n3. Updating document...")
        updated_doc = await client.update_document(
            library_id=library_id,
            document_id=doc1['id'],
            title="Introduction to Machine Learning - Updated Edition",
            metadata={"author": "John Doe", "pages": 60, "difficulty": "beginner", "edition": "2nd"}
        )
        print(f"   ✅ Updated document: {updated_doc['title']}")
        print(f"   🏷️  New metadata: {updated_doc['metadata']}")
        
        return doc1['id'], doc2['id']
        
    finally:
        await client.close()


async def demonstrate_chunk_crud(library_id: UUID, document_id: UUID):
    """Demonstrate Chunk CRUD operations."""
    print("\n🧩 Chunk CRUD Operations")
    print("=" * 50)
    
    client = VectorDBClient()
    
    try:
        # Create chunks
        print("1. Creating chunks...")
        chunk1 = await client.create_chunk(
            library_id=library_id,
            document_id=document_id,
            text="Machine learning algorithms can be supervised, unsupervised, or reinforcement learning.",
            metadata={"section": "introduction", "topic": "algorithms", "importance": "high"}
        )
        print(f"   ✅ Created chunk: {chunk1['text'][:50]}...")
        
        chunk2 = await client.create_chunk(
            library_id=library_id,
            document_id=document_id,
            text="Supervised learning uses labeled training data to learn a mapping from inputs to outputs.",
            metadata={"section": "supervised", "topic": "learning_types", "importance": "high"}
        )
        print(f"   ✅ Created chunk: {chunk2['text'][:50]}...")
        
        chunk3 = await client.create_chunk(
            library_id=library_id,
            document_id=document_id,
            text="Unsupervised learning finds hidden patterns in data without labeled examples.",
            metadata={"section": "unsupervised", "topic": "learning_types", "importance": "medium"}
        )
        print(f"   ✅ Created chunk: {chunk3['text'][:50]}...")
        
        # Read chunks
        print("\n2. Reading chunks...")
        all_chunks = await client.get_chunks(library_id, document_id)
        print(f"   🧩 Total chunks: {len(all_chunks)}")
        for i, chunk in enumerate(all_chunks, 1):
            print(f"   {i}. {chunk['text'][:60]}...")
            print(f"      🏷️  Metadata: {chunk['metadata']}")
        
        # Get specific chunk
        chunk1_details = await client.get_chunk(library_id, document_id, chunk1['id'])
        print(f"\n   📖 Chunk details: {chunk1_details['text']}")
        print(f"   🏷️  Metadata: {chunk1_details['metadata']}")
        
        # Update chunk
        print("\n3. Updating chunk...")
        updated_chunk = await client.update_chunk(
            library_id=library_id,
            document_id=document_id,
            chunk_id=chunk1['id'],
            text="Machine learning algorithms can be categorized as supervised, unsupervised, or reinforcement learning approaches.",
            metadata={"section": "introduction", "topic": "algorithms", "importance": "high", "updated": True}
        )
        print(f"   ✅ Updated chunk: {updated_chunk['text']}")
        print(f"   🏷️  New metadata: {updated_chunk['metadata']}")
        
        return [chunk1['id'], chunk2['id'], chunk3['id']]
        
    finally:
        await client.close()


async def demonstrate_search_operations(library_id: UUID):
    """Demonstrate search operations."""
    print("\n🔍 Search Operations")
    print("=" * 50)
    
    client = VectorDBClient()
    
    try:
        # Build search index
        print("1. Building search index...")
        index_result = await client.build_index(library_id)
        print(f"   ✅ Index built: {index_result}")
        
        # Wait a moment for indexing to complete
        await asyncio.sleep(2)
        
        # Search queries
        print("\n2. Performing searches...")
        
        # Search for machine learning concepts
        search1 = await client.search(
            library_id=library_id,
            query_text="machine learning algorithms",
            k=5
        )
        print(f"   🔍 Search: 'machine learning algorithms'")
        print(f"   📊 Found {search1['total_results']} results in {search1['search_time_ms']:.2f}ms")
        for i, result in enumerate(search1['results'][:3], 1):
            print(f"   {i}. Score: {result['similarity_score']:.3f} - {result['chunk']['text'][:80]}...")
        
        # Search with metadata filter
        search2 = await client.search(
            library_id=library_id,
            query_text="learning types",
            k=3,
            metadata_filter={"topic": "learning_types"}
        )
        print(f"\n   🔍 Search: 'learning types' (filtered by topic)")
        print(f"   📊 Found {search2['total_results']} results in {search2['search_time_ms']:.2f}ms")
        for i, result in enumerate(search2['results'], 1):
            print(f"   {i}. Score: {result['similarity_score']:.3f} - {result['chunk']['text'][:80]}...")
        
        # Search for specific concepts
        search3 = await client.search(
            library_id=library_id,
            query_text="supervised learning",
            k=2
        )
        print(f"\n   🔍 Search: 'supervised learning'")
        print(f"   📊 Found {search3['total_results']} results in {search3['search_time_ms']:.2f}ms")
        for i, result in enumerate(search3['results'], 1):
            print(f"   {i}. Score: {result['similarity_score']:.3f} - {result['chunk']['text'][:80]}...")
        
    finally:
        await client.close()


async def demonstrate_cascade_deletion(library_id: UUID, document_id: UUID, chunk_ids: List[UUID]):
    """Demonstrate cascade deletion operations."""
    print("\n🗑️  Cascade Deletion Operations")
    print("=" * 50)
    
    client = VectorDBClient()
    
    try:
        # Show initial state
        print("1. Initial state...")
        chunks = await client.get_chunks(library_id, document_id)
        print(f"   🧩 Chunks in document: {len(chunks)}")
        
        # Delete a chunk
        print("\n2. Deleting a chunk...")
        deleted = await client.delete_chunk(library_id, document_id, chunk_ids[0])
        if deleted:
            print(f"   ✅ Deleted chunk {chunk_ids[0]}")
        
        remaining_chunks = await client.get_chunks(library_id, document_id)
        print(f"   🧩 Remaining chunks: {len(remaining_chunks)}")
        
        # Delete document (should cascade delete all chunks)
        print("\n3. Deleting document (cascade delete chunks)...")
        deleted = await client.delete_document(library_id, document_id)
        if deleted:
            print(f"   ✅ Deleted document {document_id}")
        
        # Verify chunks are deleted
        try:
            chunks_after = await client.get_chunks(library_id, document_id)
            print(f"   🧩 Chunks after document deletion: {len(chunks_after)}")
        except httpx.HTTPStatusError:
            print(f"   ✅ Document and chunks successfully deleted (404 expected)")
        
        # Delete library (should cascade delete all documents and chunks)
        print("\n4. Deleting library (cascade delete everything)...")
        deleted = await client.delete_library(library_id)
        if deleted:
            print(f"   ✅ Deleted library {library_id}")
        
        # Verify library is deleted
        try:
            library = await client.get_library(library_id)
            print(f"   ❌ Library still exists: {library['name']}")
        except httpx.HTTPStatusError:
            print(f"   ✅ Library successfully deleted (404 expected)")
        
    finally:
        await client.close()


async def demonstrate_export_operations():
    """Demonstrate export operations."""
    print("\n📊 Export Operations")
    print("=" * 50)
    
    client = VectorDBClient()
    
    try:
        # Export CSV
        print("1. Exporting data to CSV...")
        csv_data = await client.export_csv()
        print(f"   ✅ CSV export completed")
        print(f"   📄 CSV size: {len(csv_data)} characters")
        print(f"   📝 First 200 characters:")
        print(f"   {csv_data[:200]}...")
        
    finally:
        await client.close()


async def demonstrate_error_handling():
    """Demonstrate error handling."""
    print("\n⚠️  Error Handling")
    print("=" * 50)
    
    client = VectorDBClient()
    
    try:
        # Try to get non-existent library
        print("1. Testing non-existent library...")
        try:
            fake_id = "00000000-0000-0000-0000-000000000000"
            await client.get_library(fake_id)
        except httpx.HTTPStatusError as e:
            print(f"   ✅ Expected error: {e.response.status_code} - {e.response.json()}")
        
        # Try to create library with invalid data
        print("\n2. Testing invalid data...")
        try:
            await client.create_library(name="")  # Empty name should fail
        except httpx.HTTPStatusError as e:
            print(f"   ✅ Expected validation error: {e.response.status_code}")
        
        # Try to search without index
        print("\n3. Testing search without index...")
        try:
            fake_library_id = "00000000-0000-0000-0000-000000000000"
            await client.search(fake_library_id, "test query")
        except httpx.HTTPStatusError as e:
            print(f"   ✅ Expected error: {e.response.status_code}")
        
    finally:
        await client.close()


async def main():
    """Main demonstration function."""
    print("🚀 Stack AI Vector Database - CRUD Examples")
    print("=" * 60)
    
    # Check API health
    client = VectorDBClient()
    try:
        health = await client.health_check()
        print(f"✅ API Health: {health['status']}")
    except Exception as e:
        print(f"❌ API not available: {e}")
        print("Please start the API server first: python -m uvicorn app.main:app --reload")
        return
    finally:
        await client.close()
    
    # Run demonstrations
    try:
        # Library CRUD
        library_id, library2_id = await demonstrate_library_crud()
        
        # Document CRUD
        document_id, document2_id = await demonstrate_document_crud(library_id)
        
        # Chunk CRUD
        chunk_ids = await demonstrate_chunk_crud(library_id, document_id)
        
        # Search Operations
        await demonstrate_search_operations(library_id)
        
        # Export Operations
        await demonstrate_export_operations()
        
        # Error Handling
        await demonstrate_error_handling()
        
        # Cascade Deletion
        await demonstrate_cascade_deletion(library_id, document_id, chunk_ids)
        
        print("\n🎉 All demonstrations completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
