# Vector Database Backend

A REST API for indexing and querying documents within a Vector Database, built with FastAPI and Python. This implementation follows SOLID principles and domain-driven design to create a scalable, maintainable vector search system.

## 🎯 Project Overview

This project implements a complete vector database backend with:
- **Custom indexing algorithms** (Flat and IVF-Flat) built from scratch
- **Cohere API integration** for text-to-vector embeddings
- **Thread-safe operations** with proper concurrency control
- **Comprehensive CRUD operations** for Libraries, Documents, and Chunks
- **k-NN vector similarity search** with metadata filtering
- **RESTful API** with proper HTTP status codes

## 📁 Project Structure

```
vector_db/
├── app/                       # Main application code
│   ├── main.py               # FastAPI application entry point
│   ├── config.py             # Configuration settings
│   ├── models/               # Pydantic models
│   ├── services/             # Business logic layer
│   ├── repositories/         # Data access layer
│   ├── indexing/             # Custom indexing algorithms
│   ├── api/                  # API endpoints
│   └── utils/                # Utility functions
├── tests/                    # Unit tests
│   ├── test_models.py        # Model tests
│   └── test_indexing.py      # Indexing algorithm tests
├── requirements.txt          # Python dependencies
├── setup_and_run.sh         # Setup and run script
├── run_tests.py             # Test runner
└── README.md                # This file
```

## 🏗️ Architecture & Design Principles

### SOLID Principles Implementation

1. **Single Responsibility**: Each class has one clear purpose
   - `LibraryService` handles only library business logic
   - `FlatIndex` handles only brute force indexing
   - `EmbeddingService` handles only text-to-vector conversion

2. **Open/Closed**: Extensible without modification
   - `BaseIndex` allows new indexing algorithms without changing existing code
   - `BaseRepository` allows different storage backends

3. **Liskov Substitution**: Subtypes are substitutable for base types
   - All index implementations can be used interchangeably
   - Repository implementations follow the same interface

4. **Interface Segregation**: Clients depend only on interfaces they use
   - Separate interfaces for different operations
   - Minimal dependencies between components

5. **Dependency Inversion**: Depend on abstractions, not concretions
   - Services depend on repository interfaces, not implementations
   - Indexing algorithms depend on abstract base classes

### Domain-Driven Design

- **API Layer**: FastAPI endpoints with proper HTTP status codes
- **Service Layer**: Business logic and orchestration
- **Repository Layer**: Data access and persistence
- **Domain Models**: Pydantic models with validation

### Concurrency Safety

- **Thread-Safe Collections**: Custom implementations for safe concurrent access
- **Async Operations**: Non-blocking I/O for better performance
- **Proper Locking**: RLock for recursive operations, preventing deadlocks

## 🔍 Core Features

### 1. CRUD Operations
- **Libraries**: Create, read, update, delete library collections
- **Documents**: Manage documents within libraries
- **Chunks**: Handle text chunks with automatic embedding generation

### 2. Vector Embeddings
- **Cohere Integration**: Uses Cohere's `embed-english-v3.0` model
- **Automatic Generation**: Embeddings created when chunks are added
- **Query Optimization**: Separate embeddings for search queries vs documents

### 3. Custom Indexing Algorithms

#### Flat Index (Brute Force)
- **Algorithm**: Linear scan with cosine similarity
- **Build Time**: O(n) - Simple vector storage
- **Search Time**: O(n) - Compare query with all vectors
- **Space**: O(n*d) - Store all vectors in memory
- **Use Case**: Small datasets, exact results required

#### IVF-Flat Index (Inverted File Index)
- **Algorithm**: K-Means clustering + approximate search
- **Build Time**: O(n*log(n)) - K-Means clustering overhead
- **Search Time**: O(k + n/k) - Search only relevant clusters
- **Space**: O(n*d + k*d) - Vectors + cluster centroids
- **Use Case**: Large datasets, approximate results acceptable

### 4. k-NN Search
- **Vector Similarity**: Cosine similarity for semantic search
- **Configurable k**: Return top-k most similar chunks
- **Metadata Filtering**: Optional filters for refined results
- **Multiple Index Types**: Choose between Flat or IVF indexing

### 5. Concurrency Control
- **Thread-Safe Operations**: Safe concurrent reads/writes
- **Race Condition Prevention**: Proper locking mechanisms
- **Async Support**: Non-blocking operations

## 📊 Complexity Analysis

### Time Complexity

| Operation | Flat Index | IVF-Flat Index |
|-----------|------------|----------------|
| Build | O(n) | O(n*log(n)) |
| Search | O(n) | O(k + n/k) |
| Insert | O(1) | O(1) |
| Delete | O(1) | O(1) |

### Space Complexity

| Component | Flat Index | IVF-Flat Index |
|-----------|------------|----------------|
| Vectors | O(n*d) | O(n*d) |
| Index Structure | O(1) | O(k*d) |
| Total | O(n*d) | O(n*d + k*d) |

### Performance Trade-offs

**Flat Index Advantages:**
- Exact results (100% recall)
- Simple implementation
- No clustering overhead
- Predictable performance

**Flat Index Disadvantages:**
- Linear search time
- Not scalable for large datasets
- High memory usage

**IVF-Flat Index Advantages:**
- Faster search for large datasets
- Better scalability
- Lower memory per query
- Approximate results acceptable

**IVF-Flat Index Disadvantages:**
- Approximate results (recall < 100%)
- Complex implementation
- Clustering overhead
- Parameter tuning required

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Cohere API key (provided in config)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd vector_db

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Quick Setup (Recommended)
```bash
# Run the setup script (handles everything automatically)
./setup_and_run.sh
```

#### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option 3: Using pipx (Alternative)
```bash
# Install pipx if not already installed
brew install pipx

# Install dependencies
pipx install fastapi uvicorn pydantic numpy cohere

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API

```bash
# Run the test suite (make sure API is running first)
python test_api.py

# Or run unit tests
python run_tests.py
```

### Running Tests

```bash
# Run all tests
python run_tests.py

# Or use pytest directly
pytest tests/ -v
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Core Endpoints

#### Libraries
```
POST   /libraries                    # Create library
GET    /libraries                    # List all libraries
GET    /libraries/{id}               # Get library
PUT    /libraries/{id}               # Update library
DELETE /libraries/{id}               # Delete library
```

#### Documents
```
POST   /libraries/{id}/documents      # Create document
GET    /libraries/{id}/documents      # List documents in library
GET    /libraries/{id}/documents/{doc_id}  # Get document
PUT    /libraries/{id}/documents/{doc_id}   # Update document
DELETE /libraries/{id}/documents/{doc_id}  # Delete document
```

#### Chunks
```
POST   /libraries/{id}/documents/{doc_id}/chunks  # Create chunk
GET    /libraries/{id}/documents/{doc_id}/chunks  # List chunks in document
GET    /libraries/{id}/documents/{doc_id}/chunks/{chunk_id}  # Get chunk
PUT    /libraries/{id}/documents/{doc_id}/chunks/{chunk_id}  # Update chunk
DELETE /libraries/{id}/documents/{doc_id}/chunks/{chunk_id}  # Delete chunk
```

#### Search
```
POST   /libraries/{id}/search         # k-NN vector search
POST   /libraries/{id}/index          # Build indexes
GET    /libraries/{id}/index/stats    # Get index statistics
POST   /libraries/{id}/index/rebuild  # Rebuild indexes
GET    /libraries/{id}/index/available # Get available indexes
```

### Example Usage

#### 1. Create a Library
```bash
curl -X POST "http://localhost:8000/libraries" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Research Papers",
    "description": "Collection of AI research papers",
    "metadata": {"category": "research"}
  }'
```

#### 2. Add a Document
```bash
curl -X POST "http://localhost:8000/libraries/{library_id}/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Attention Is All You Need",
    "content": "The dominant sequence transduction models...",
    "metadata": {"authors": ["Vaswani", "Shazeer"], "year": 2017}
  }'
```

#### 3. Add Chunks
```bash
curl -X POST "http://localhost:8000/libraries/{library_id}/documents/{doc_id}/chunks" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The Transformer architecture is based solely on attention mechanisms...",
    "metadata": {"section": "introduction"}
  }'
```

#### 4. Build Indexes
```bash
curl -X POST "http://localhost:8000/libraries/{library_id}/index"
```

#### 5. Search
```bash
curl -X POST "http://localhost:8000/libraries/{library_id}/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "What is attention mechanism?",
    "k": 5,
    "metadata_filter": {"section": "introduction"}
  }'
```

## 🧪 Testing

### Test Coverage
- **Models**: Pydantic validation and serialization
- **Indexing**: Both Flat and IVF algorithms
- **Services**: Business logic and error handling
- **API**: Endpoint functionality and status codes

### Running Tests
```bash
# Run all tests
python run_tests.py

# Run specific test file
pytest tests/test_indexing.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## 🔧 Configuration

### Environment Variables
```bash
# Cohere API Configuration
COHERE_API_KEY=pa6sRhnVAedMVClPAwoCvC1MjHKEwjtcGSTjWRMd
COHERE_MODEL=embed-english-v3.0

# Vector Configuration
EMBEDDING_DIMENSION=1024
MAX_CHUNK_SIZE=1000
DEFAULT_K=10

# Indexing Configuration
IVF_N_CLUSTERS=100
IVF_MAX_ITERATIONS=100

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

## 🚀 Performance Considerations

### Optimization Strategies
1. **Batch Operations**: Process multiple chunks simultaneously
2. **Index Caching**: Keep frequently used indexes in memory
3. **Async Operations**: Non-blocking I/O for better throughput
4. **Connection Pooling**: Reuse HTTP connections to Cohere API

### Scalability
- **Horizontal Scaling**: Stateless design allows multiple instances
- **Index Partitioning**: Split large indexes across multiple nodes
- **Caching**: Redis for frequently accessed data
- **Load Balancing**: Distribute requests across instances

## 🔮 Future Enhancements

### Planned Features
1. **Persistence**: Save indexes to disk for durability
2. **Metadata Filtering**: Advanced filtering capabilities
3. **Leader-Follower**: Distributed architecture for high availability
4. **Python SDK**: Client library for easier integration
5. **Temporal Integration**: Durable execution workflows

### Performance Improvements
1. **GPU Acceleration**: CUDA support for faster computations
2. **Quantization**: Reduce memory usage with compressed vectors
3. **Hierarchical Indexing**: Multi-level clustering for better recall
4. **Approximate Algorithms**: LSH and other approximate methods

## 📄 License

This project is part of a technical assessment and is not intended for production use.

## 🤝 Contributing

This is a take-home assignment implementation. For questions or feedback, please contact the development team.

---

**Built with ❤️ using FastAPI, Pydantic, and custom vector indexing algorithms**
