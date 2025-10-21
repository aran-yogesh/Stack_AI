# API Usage Examples

This document provides comprehensive examples of how to use the Stack AI Vector Database API with both cURL and Python.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Library Operations](#library-operations)
3. [Document Operations](#document-operations)
4. [Chunk Operations](#chunk-operations)
5. [Search Operations](#search-operations)
6. [Export Operations](#export-operations)
7. [Error Handling](#error-handling)
8. [Python Client Examples](#python-client-examples)
9. [Advanced Usage](#advanced-usage)

## Quick Start

### Start the API Server

```bash
# Start the server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Check health
curl http://localhost:8000/health
```

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Library Operations

### Create a Library

**cURL:**
```bash
curl -X POST "http://localhost:8000/libraries/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Machine Learning Papers",
    "description": "A collection of ML research papers",
    "metadata": {
      "category": "AI",
      "version": "1.0",
      "tags": ["machine-learning", "research"]
    }
  }'
```

**Python:**
```python
import httpx
import asyncio

async def create_library():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/libraries/",
            json={
                "name": "Machine Learning Papers",
                "description": "A collection of ML research papers",
                "metadata": {
                    "category": "AI",
                    "version": "1.0",
                    "tags": ["machine-learning", "research"]
                }
            }
        )
        return response.json()

# Run the function
library = asyncio.run(create_library())
print(f"Created library: {library['name']} (ID: {library['id']})")
```

### Get All Libraries

**cURL:**
```bash
curl -X GET "http://localhost:8000/libraries/"
```

**Python:**
```python
async def get_all_libraries():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/libraries/")
        return response.json()

libraries = asyncio.run(get_all_libraries())
for lib in libraries:
    print(f"- {lib['name']}: {lib['description']}")
```

### Get Library by ID

**cURL:**
```bash
curl -X GET "http://localhost:8000/libraries/{library_id}"
```

**Python:**
```python
async def get_library(library_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/libraries/{library_id}")
        return response.json()

library = asyncio.run(get_library("your-library-id"))
print(f"Library: {library['name']}")
```

### Update Library

**cURL:**
```bash
curl -X PUT "http://localhost:8000/libraries/{library_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated ML Papers",
    "description": "Updated collection of ML research papers",
    "metadata": {
      "category": "AI",
      "version": "2.0",
      "tags": ["machine-learning", "research", "updated"]
    }
  }'
```

**Python:**
```python
async def update_library(library_id):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"http://localhost:8000/libraries/{library_id}",
            json={
                "name": "Updated ML Papers",
                "description": "Updated collection of ML research papers",
                "metadata": {
                    "category": "AI",
                    "version": "2.0",
                    "tags": ["machine-learning", "research", "updated"]
                }
            }
        )
        return response.json()

updated_library = asyncio.run(update_library("your-library-id"))
```

### Delete Library

**cURL:**
```bash
curl -X DELETE "http://localhost:8000/libraries/{library_id}"
```

**Python:**
```python
async def delete_library(library_id):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"http://localhost:8000/libraries/{library_id}")
        return response.status_code == 204

deleted = asyncio.run(delete_library("your-library-id"))
print(f"Library deleted: {deleted}")
```

## Document Operations

### Create a Document

**cURL:**
```bash
curl -X POST "http://localhost:8000/libraries/{library_id}/documents/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Deep Learning",
    "content": "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model and understand complex patterns in data.",
    "metadata": {
      "author": "Dr. Jane Smith",
      "year": 2023,
      "pages": 45,
      "difficulty": "intermediate",
      "topics": ["deep-learning", "neural-networks", "machine-learning"]
    }
  }'
```

**Python:**
```python
async def create_document(library_id):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:8000/libraries/{library_id}/documents/",
            json={
                "title": "Introduction to Deep Learning",
                "content": "Deep learning is a subset of machine learning that uses neural networks with multiple layers to model and understand complex patterns in data.",
                "metadata": {
                    "author": "Dr. Jane Smith",
                    "year": 2023,
                    "pages": 45,
                    "difficulty": "intermediate",
                    "topics": ["deep-learning", "neural-networks", "machine-learning"]
                }
            }
        )
        return response.json()

document = asyncio.run(create_document("your-library-id"))
print(f"Created document: {document['title']} (ID: {document['id']})")
```

### Get All Documents in Library

**cURL:**
```bash
curl -X GET "http://localhost:8000/libraries/{library_id}/documents/"
```

**Python:**
```python
async def get_documents(library_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/libraries/{library_id}/documents/")
        return response.json()

documents = asyncio.run(get_documents("your-library-id"))
for doc in documents:
    print(f"- {doc['title']} by {doc['metadata'].get('author', 'Unknown')}")
```

### Get Document by ID

**cURL:**
```bash
curl -X GET "http://localhost:8000/libraries/{library_id}/documents/{document_id}"
```

**Python:**
```python
async def get_document(library_id, document_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/libraries/{library_id}/documents/{document_id}")
        return response.json()

document = asyncio.run(get_document("your-library-id", "your-document-id"))
print(f"Document: {document['title']}")
print(f"Content: {document['content']}")
```

### Update Document

**cURL:**
```bash
curl -X PUT "http://localhost:8000/libraries/{library_id}/documents/{document_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced Deep Learning Concepts",
    "content": "Updated content about advanced deep learning concepts...",
    "metadata": {
      "author": "Dr. Jane Smith",
      "year": 2024,
      "pages": 50,
      "difficulty": "advanced",
      "topics": ["deep-learning", "neural-networks", "machine-learning", "advanced"]
    }
  }'
```

**Python:**
```python
async def update_document(library_id, document_id):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"http://localhost:8000/libraries/{library_id}/documents/{document_id}",
            json={
                "title": "Advanced Deep Learning Concepts",
                "content": "Updated content about advanced deep learning concepts...",
                "metadata": {
                    "author": "Dr. Jane Smith",
                    "year": 2024,
                    "pages": 50,
                    "difficulty": "advanced",
                    "topics": ["deep-learning", "neural-networks", "machine-learning", "advanced"]
                }
            }
        )
        return response.json()

updated_document = asyncio.run(update_document("your-library-id", "your-document-id"))
```

### Delete Document

**cURL:**
```bash
curl -X DELETE "http://localhost:8000/libraries/{library_id}/documents/{document_id}"
```

**Python:**
```python
async def delete_document(library_id, document_id):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"http://localhost:8000/libraries/{library_id}/documents/{document_id}")
        return response.status_code == 204

deleted = asyncio.run(delete_document("your-library-id", "your-document-id"))
print(f"Document deleted: {deleted}")
```

## Chunk Operations

### Create a Chunk

**cURL:**
```bash
curl -X POST "http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information using a connectionist approach to computation.",
    "metadata": {
      "section": "introduction",
      "topic": "neural-networks",
      "importance": "high",
      "page": 1
    }
  }'
```

**Python:**
```python
async def create_chunk(library_id, document_id):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/",
            json={
                "text": "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information using a connectionist approach to computation.",
                "metadata": {
                    "section": "introduction",
                    "topic": "neural-networks",
                    "importance": "high",
                    "page": 1
                }
            }
        )
        return response.json()

chunk = asyncio.run(create_chunk("your-library-id", "your-document-id"))
print(f"Created chunk: {chunk['text'][:50]}...")
```

### Get All Chunks in Document

**cURL:**
```bash
curl -X GET "http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/"
```

**Python:**
```python
async def get_chunks(library_id, document_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/")
        return response.json()

chunks = asyncio.run(get_chunks("your-library-id", "your-document-id"))
for i, chunk in enumerate(chunks, 1):
    print(f"{i}. {chunk['text'][:100]}...")
    print(f"   Metadata: {chunk['metadata']}")
```

### Get Chunk by ID

**cURL:**
```bash
curl -X GET "http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}"
```

**Python:**
```python
async def get_chunk(library_id, document_id, chunk_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}")
        return response.json()

chunk = asyncio.run(get_chunk("your-library-id", "your-document-id", "your-chunk-id"))
print(f"Chunk: {chunk['text']}")
```

### Update Chunk

**cURL:**
```bash
curl -X PUT "http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Updated text about neural networks and their applications in deep learning.",
    "metadata": {
      "section": "introduction",
      "topic": "neural-networks",
      "importance": "high",
      "page": 1,
      "updated": true
    }
  }'
```

**Python:**
```python
async def update_chunk(library_id, document_id, chunk_id):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}",
            json={
                "text": "Updated text about neural networks and their applications in deep learning.",
                "metadata": {
                    "section": "introduction",
                    "topic": "neural-networks",
                    "importance": "high",
                    "page": 1,
                    "updated": True
                }
            }
        )
        return response.json()

updated_chunk = asyncio.run(update_chunk("your-library-id", "your-document-id", "your-chunk-id"))
```

### Delete Chunk

**cURL:**
```bash
curl -X DELETE "http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}"
```

**Python:**
```python
async def delete_chunk(library_id, document_id, chunk_id):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}")
        return response.status_code == 204

deleted = asyncio.run(delete_chunk("your-library-id", "your-document-id", "your-chunk-id"))
print(f"Chunk deleted: {deleted}")
```

## Search Operations

### Build Search Index

**cURL:**
```bash
curl -X POST "http://localhost:8000/libraries/{library_id}/index"
```

**Python:**
```python
async def build_index(library_id):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:8000/libraries/{library_id}/index")
        return response.json()

index_result = asyncio.run(build_index("your-library-id"))
print(f"Index built: {index_result}")
```

### Search Chunks

**cURL:**
```bash
curl -X POST "http://localhost:8000/libraries/{library_id}/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "neural networks deep learning",
    "k": 10,
    "metadata_filter": {
      "topic": "neural-networks"
    }
  }'
```

**Python:**
```python
async def search_chunks(library_id, query_text, k=10, metadata_filter=None):
    async with httpx.AsyncClient() as client:
        search_data = {
            "query_text": query_text,
            "k": k
        }
        if metadata_filter:
            search_data["metadata_filter"] = metadata_filter
        
        response = await client.post(f"http://localhost:8000/libraries/{library_id}/search", json=search_data)
        return response.json()

# Basic search
results = asyncio.run(search_chunks("your-library-id", "neural networks deep learning", k=10))
print(f"Found {results['total_results']} results in {results['search_time_ms']:.2f}ms")

# Search with metadata filter
filtered_results = asyncio.run(search_chunks(
    "your-library-id", 
    "neural networks", 
    k=5, 
    metadata_filter={"topic": "neural-networks"}
))
print(f"Filtered results: {filtered_results['total_results']} results")
```

### Advanced Search Examples

**Search with multiple metadata filters:**
```python
async def advanced_search(library_id):
    async with httpx.AsyncClient() as client:
        # Search for high-importance chunks about neural networks
        search_data = {
            "query_text": "machine learning algorithms",
            "k": 20,
            "metadata_filter": {
                "importance": "high",
                "topic": "neural-networks"
            }
        }
        response = await client.post(f"http://localhost:8000/libraries/{library_id}/search", json=search_data)
        return response.json()

results = asyncio.run(advanced_search("your-library-id"))
for i, result in enumerate(results['results'][:5], 1):
    print(f"{i}. Score: {result['similarity_score']:.3f}")
    print(f"   Text: {result['chunk']['text'][:100]}...")
    print(f"   Metadata: {result['chunk']['metadata']}")
    print()
```

## Export Operations

### Export to CSV

**cURL:**
```bash
curl -X GET "http://localhost:8000/csv/export" -o data_export.csv
```

**Python:**
```python
async def export_csv():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/csv/export")
        return response.text

csv_data = asyncio.run(export_csv())
print(f"CSV export size: {len(csv_data)} characters")

# Save to file
with open("data_export.csv", "w") as f:
    f.write(csv_data)
print("CSV exported to data_export.csv")
```

## Error Handling

### Common Error Responses

**404 Not Found:**
```json
{
  "error": "Library with ID 00000000-0000-0000-0000-000000000000 not found",
  "status_code": 404
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length",
      "ctx": {"limit_value": 1}
    }
  ]
}
```

**409 Conflict:**
```json
{
  "error": "Library with name 'Existing Library' already exists",
  "status_code": 409
}
```

### Python Error Handling

```python
import httpx

async def safe_api_call():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/libraries/nonexistent-id")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print("Resource not found")
            elif e.response.status_code == 422:
                print("Validation error:", e.response.json())
            else:
                print(f"HTTP error: {e.response.status_code}")
        except httpx.RequestError as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

asyncio.run(safe_api_call())
```

## Python Client Examples

### Complete Python Client Class

```python
import httpx
import asyncio
from typing import List, Dict, Any, Optional
from uuid import UUID

class VectorDBClient:
    """Complete client for Vector Database API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    # Library methods
    async def create_library(self, name: str, description: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new library."""
        data = {"name": name}
        if description:
            data["description"] = description
        if metadata:
            data["metadata"] = metadata
        
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
    
    async def update_library(self, library_id: UUID, **kwargs) -> Dict[str, Any]:
        """Update a library."""
        response = await self.client.put(f"{self.base_url}/libraries/{library_id}", json=kwargs)
        response.raise_for_status()
        return response.json()
    
    async def delete_library(self, library_id: UUID) -> bool:
        """Delete a library."""
        response = await self.client.delete(f"{self.base_url}/libraries/{library_id}")
        response.raise_for_status()
        return response.status_code == 204
    
    # Document methods
    async def create_document(self, library_id: UUID, title: str, content: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new document."""
        data = {"title": title}
        if content:
            data["content"] = content
        if metadata:
            data["metadata"] = metadata
        
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
    
    async def update_document(self, library_id: UUID, document_id: UUID, **kwargs) -> Dict[str, Any]:
        """Update a document."""
        response = await self.client.put(f"{self.base_url}/libraries/{library_id}/documents/{document_id}", json=kwargs)
        response.raise_for_status()
        return response.json()
    
    async def delete_document(self, library_id: UUID, document_id: UUID) -> bool:
        """Delete a document."""
        response = await self.client.delete(f"{self.base_url}/libraries/{library_id}/documents/{document_id}")
        response.raise_for_status()
        return response.status_code == 204
    
    # Chunk methods
    async def create_chunk(self, library_id: UUID, document_id: UUID, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new chunk."""
        data = {"text": text}
        if metadata:
            data["metadata"] = metadata
        
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
    
    async def update_chunk(self, library_id: UUID, document_id: UUID, chunk_id: UUID, **kwargs) -> Dict[str, Any]:
        """Update a chunk."""
        response = await self.client.put(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}", json=kwargs)
        response.raise_for_status()
        return response.json()
    
    async def delete_chunk(self, library_id: UUID, document_id: UUID, chunk_id: UUID) -> bool:
        """Delete a chunk."""
        response = await self.client.delete(f"{self.base_url}/libraries/{library_id}/documents/{document_id}/chunks/{chunk_id}")
        response.raise_for_status()
        return response.status_code == 204
    
    # Search methods
    async def build_index(self, library_id: UUID) -> Dict[str, Any]:
        """Build search index for a library."""
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/index")
        response.raise_for_status()
        return response.json()
    
    async def search(self, library_id: UUID, query_text: str, k: int = 10, metadata_filter: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search for similar chunks."""
        data = {"query_text": query_text, "k": k}
        if metadata_filter:
            data["metadata_filter"] = metadata_filter
        
        response = await self.client.post(f"{self.base_url}/libraries/{library_id}/search", json=data)
        response.raise_for_status()
        return response.json()
    
    # Utility methods
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

# Usage example
async def main():
    client = VectorDBClient()
    
    try:
        # Create library
        library = await client.create_library(
            name="Test Library",
            description="A test library",
            metadata={"test": True}
        )
        print(f"Created library: {library['name']}")
        
        # Create document
        document = await client.create_document(
            library_id=library['id'],
            title="Test Document",
            content="This is a test document.",
            metadata={"author": "Test Author"}
        )
        print(f"Created document: {document['title']}")
        
        # Create chunk
        chunk = await client.create_chunk(
            library_id=library['id'],
            document_id=document['id'],
            text="This is a test chunk.",
            metadata={"section": "test"}
        )
        print(f"Created chunk: {chunk['text']}")
        
        # Build index and search
        await client.build_index(library['id'])
        results = await client.search(library['id'], "test chunk", k=5)
        print(f"Search results: {results['total_results']} found")
        
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Advanced Usage

### Batch Operations

```python
async def batch_create_chunks(client, library_id, document_id, chunks_data):
    """Create multiple chunks in batch."""
    tasks = []
    for chunk_data in chunks_data:
        task = client.create_chunk(library_id, document_id, chunk_data['text'], chunk_data.get('metadata'))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results

# Usage
chunks_data = [
    {"text": "First chunk", "metadata": {"section": "1"}},
    {"text": "Second chunk", "metadata": {"section": "2"}},
    {"text": "Third chunk", "metadata": {"section": "3"}}
]

chunks = await batch_create_chunks(client, library_id, document_id, chunks_data)
print(f"Created {len(chunks)} chunks")
```

### Concurrent Search

```python
async def concurrent_search(client, library_id, queries):
    """Perform multiple searches concurrently."""
    tasks = []
    for query in queries:
        task = client.search(library_id, query, k=5)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results

# Usage
queries = [
    "machine learning",
    "deep learning",
    "neural networks",
    "artificial intelligence"
]

search_results = await concurrent_search(client, library_id, queries)
for i, result in enumerate(search_results):
    print(f"Query {i+1}: {result['total_results']} results")
```

### Data Migration

```python
async def migrate_data(source_client, target_client, library_id):
    """Migrate data from one instance to another."""
    # Get all data from source
    library = await source_client.get_library(library_id)
    documents = await source_client.get_documents(library_id)
    
    # Create library in target
    new_library = await target_client.create_library(
        name=library['name'],
        description=library['description'],
        metadata=library['metadata']
    )
    
    # Migrate documents and chunks
    for document in documents:
        new_document = await target_client.create_document(
            library_id=new_library['id'],
            title=document['title'],
            content=document['content'],
            metadata=document['metadata']
        )
        
        chunks = await source_client.get_chunks(library_id, document['id'])
        for chunk in chunks:
            await target_client.create_chunk(
                library_id=new_library['id'],
                document_id=new_document['id'],
                text=chunk['text'],
                metadata=chunk['metadata']
            )
    
    return new_library['id']
```

This comprehensive guide provides everything needed to effectively use the Stack AI Vector Database API with both cURL and Python.
