#!/usr/bin/env python3
"""
Simple CRUD Example for Stack AI Vector Database

This script demonstrates basic CRUD operations with the Vector Database API.

Usage:
    python examples/simple_crud_example.py
"""

import asyncio
from typing import Any, Dict, Optional
from uuid import UUID

import httpx


class SimpleVectorDBClient:
    """Simple client for Vector Database API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def create_library(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new library."""
        data = {"name": name}
        if description:
            data["description"] = description

        response = await self.client.post(f"{self.base_url}/libraries/", json=data)
        response.raise_for_status()
        return response.json()

    async def get_library(self, library_id: UUID) -> Dict[str, Any]:
        """Get a library by ID."""
        response = await self.client.get(f"{self.base_url}/libraries/{library_id}")
        response.raise_for_status()
        return response.json()

    async def create_document(self, library_id: UUID, title: str, content: Optional[str] = None) -> Dict[str, Any]:
        """Create a new document."""
        data = {"title": title}
        if content:
            data["content"] = content

        response = await self.client.post(
            f"{self.base_url}/libraries/{library_id}/documents/", json=data
        )
        response.raise_for_status()
        return response.json()

    async def create_chunk(self, library_id: UUID, document_id: UUID, text: str) -> Dict[str, Any]:
        """Create a new chunk."""
        data = {"text": text}

        response = await self.client.post(
            f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/",
            json=data
        )
        response.raise_for_status()
        return response.json()

    async def build_index(self, library_id: UUID) -> Dict[str, Any]:
        """Build search index for a library."""
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/index")
        response.raise_for_status()
        return response.json()

    async def search(self, library_id: UUID, query_text: str, k: int = 5) -> Dict[str, Any]:
        """Search for similar chunks."""
        data = {"query_text": query_text, "k": k}

        response = await self.client.post(
            f"{self.base_url}/libraries/{library_id}/search", json=data
        )
        response.raise_for_status()
        return response.json()

    async def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        response = await self.client.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()


async def main():
    """Main demonstration function."""
    print("🚀 Simple CRUD Example")
    print("=" * 40)

    client = SimpleVectorDBClient()

    try:
        # Check API health
        health = await client.health_check()
        print(f"✅ API Health: {health['status']}")

        # Create library
        print("\n1. Creating library...")
        library = await client.create_library(
            name="Test Library",
            description="A simple test library"
        )
        print(f"✅ Created library: {library['name']} (ID: {library['id']})")

        # Create document
        print("\n2. Creating document...")
        document = await client.create_document(
            library_id=library['id'],
            title="Test Document",
            content="This is a test document about machine learning."
        )
        print(f"✅ Created document: {document['title']} (ID: {document['id']})")

        # Create chunks
        print("\n3. Creating chunks...")
        chunks_data = [
            "Machine learning is a subset of artificial intelligence.",
            "Deep learning uses neural networks with multiple layers.",
            "Natural language processing deals with text and speech data."
        ]

        chunk_ids = []
        for i, text in enumerate(chunks_data, 1):
            chunk = await client.create_chunk(
                library_id=library['id'],
                document_id=document['id'],
                text=text
            )
            chunk_ids.append(chunk['id'])
            print(f"   ✅ Created chunk {i}: {text[:50]}...")

        # Build index
        print("\n4. Building search index...")
        index_result = await client.build_index(library['id'])
        print(f"✅ Index built: {index_result}")

        # Wait for indexing
        await asyncio.sleep(2)

        # Search
        print("\n5. Performing search...")
        search_results = await client.search(
            library_id=library['id'],
            query_text="machine learning",
            k=3
        )

        print(f"✅ Found {search_results['total_results']} results in {search_results['search_time_ms']:.2f}ms")
        for i, result in enumerate(search_results['results'], 1):
            print(f"   {i}. Score: {result['similarity_score']:.3f}")
            print(f"      Text: {result['chunk']['text']}")

        print("\n🎉 Example completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure the API server is running:")
        print("  python -m uvicorn app.main:app --reload")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
