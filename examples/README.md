# Stack AI Vector Database - Examples and Testing

This directory contains comprehensive examples and testing utilities for the Stack AI Vector Database.

## 📁 Directory Structure

```
examples/
├── README.md                    # This file
├── simple_crud_example.py      # Simple CRUD example (recommended)
├── simple_test_runner.py       # Simple test runner (recommended)
├── run_tests.py                # Advanced test runner script
├── crud_examples.py            # Complete CRUD examples
├── testing_examples.py         # Comprehensive test suite
├── setup_examples.py           # Setup script
└── api_usage_examples.md       # API usage documentation
```

## 🚀 Quick Start

### 1. Start the API Server

```bash
# From the project root
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Run Examples

**Quick Start (Recommended):**
```bash
# Run simple examples and tests
python examples/simple_test_runner.py

# Run simple CRUD example only
python examples/simple_crud_example.py
```

**Advanced Examples:**
```bash
# Run all examples and tests
python examples/run_tests.py

# Run specific test types
python examples/run_tests.py --test-type crud
python examples/run_tests.py --test-type tests
python examples/run_tests.py --test-type benchmark
```

### 3. Run Individual Examples

```bash
# Simple examples (recommended for beginners)
python examples/simple_crud_example.py
python examples/simple_test_runner.py

# Advanced examples
python examples/crud_examples.py
python examples/testing_examples.py
```

## 📚 What's Included

### 1. Simple Examples (Recommended for Beginners)

#### Simple CRUD Example (`simple_crud_example.py`)
A clean, easy-to-understand example that demonstrates:
- Basic library creation
- Document creation
- Chunk creation
- Search index building
- Simple search operations
- Error handling

**Perfect for:**
- Learning the API basics
- Quick testing
- Understanding the workflow

#### Simple Test Runner (`simple_test_runner.py`)
A straightforward test runner that:
- Checks API health
- Runs basic functionality tests
- Tests all CRUD operations
- Performs search tests
- Cleans up test data

**Perfect for:**
- Quick validation
- Basic testing
- CI/CD pipelines

### 2. Advanced Examples

#### CRUD Examples (`crud_examples.py`)

Complete demonstrations of all CRUD operations:

- **Library Operations**: Create, Read, Update, Delete libraries
- **Document Operations**: Create, Read, Update, Delete documents
- **Chunk Operations**: Create, Read, Update, Delete chunks
- **Search Operations**: Build indexes and perform similarity searches
- **Cascade Deletion**: Test automatic cleanup of related entities
- **Export Operations**: Export data to CSV format
- **Error Handling**: Demonstrate proper error handling

**Key Features:**
- Easy-to-understand code examples
- Comprehensive error handling
- Real-world usage patterns
- Performance timing
- Data validation examples

### 2. Testing Examples (`testing_examples.py`)

Comprehensive test suite covering:

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Load testing and benchmarking
- **Error Handling Tests**: Validation and error scenarios
- **Concurrent Operations**: Multi-threaded testing
- **Large Dataset Testing**: Scalability testing

**Test Categories:**
- API Health Checks
- CRUD Operations Validation
- Search Functionality
- Data Consistency
- Cascade Deletion
- Concurrent Operations
- Performance Benchmarking
- Error Scenarios

### 3. API Usage Examples (`api_usage_examples.md`)

Complete API documentation with examples:

- **cURL Commands**: Command-line API usage
- **Python Examples**: Programmatic API usage
- **Complete Client Class**: Ready-to-use Python client
- **Error Handling**: Proper error management
- **Advanced Usage**: Batch operations, concurrent requests
- **Data Migration**: Moving data between instances

### 4. Test Runner (`run_tests.py`)

Convenient script to run all tests:

```bash
# Run all tests
python examples/run_tests.py

# Run specific test types
python examples/run_tests.py --test-type crud
python examples/run_tests.py --test-type tests
python examples/run_tests.py --test-type benchmark

# Skip health check
python examples/run_tests.py --skip-health-check
```

## 🧪 Testing Guide

### Running Tests

1. **Start the API Server**:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Run Tests**:
   ```bash
   # All tests
   python examples/run_tests.py
   
   # Specific tests
   python examples/run_tests.py --test-type tests
   ```

3. **Check Results**:
   - Tests will show ✅ for success
   - Tests will show ❌ for failure
   - Detailed error messages for debugging

### Test Types

#### CRUD Tests
- Test all Create, Read, Update, Delete operations
- Validate data integrity
- Test cascade deletion
- Verify error handling

#### Integration Tests
- End-to-end workflows
- Service integration
- Data consistency
- API endpoint testing

#### Performance Tests
- Concurrent operations
- Large dataset handling
- Search performance
- Memory usage

#### Benchmark Tests
- Chunk creation rate
- Index building time
- Search response time
- Throughput measurements

## 📊 Performance Benchmarks

The examples include performance benchmarks that test:

- **Chunk Creation**: Rate of chunk creation (chunks/second)
- **Index Building**: Time to build search indexes
- **Search Performance**: Query response times
- **Concurrent Operations**: Multi-threaded performance
- **Memory Usage**: Resource utilization

### Example Benchmark Results

```
📊 Performance Benchmark
============================================================
📊 Benchmarking chunk creation...
✅ Created 1000 chunks in 15.23 seconds
📈 Rate: 65.66 chunks/second

📊 Benchmarking index building...
✅ Built index in 2.45 seconds

📊 Benchmarking search performance...
   Query 'machine learning': 45 results in 0.123s
   Query 'artificial intelligence': 38 results in 0.098s
   Query 'data science': 52 results in 0.134s
   Query 'neural networks': 41 results in 0.112s
   Query 'deep learning': 39 results in 0.105s

📈 Average search time: 0.114 seconds
📈 Average results per query: 43.0
```

## 🔧 Customization

### Custom Test Data

You can customize the test data by modifying the examples:

```python
# In crud_examples.py
library_data = {
    "name": "Your Custom Library",
    "description": "Your custom description",
    "metadata": {"custom": "data"}
}

# In testing_examples.py
chunk_data = {
    "text": "Your custom text content",
    "metadata": {"custom": "metadata"}
}
```

### Custom Test Scenarios

Add your own test scenarios:

```python
async def test_custom_scenario(self):
    """Test your custom scenario."""
    # Your test code here
    pass
```

### Custom Performance Tests

Create custom performance tests:

```python
async def test_custom_performance():
    """Test custom performance scenario."""
    # Your performance test code here
    pass
```

## 🐛 Troubleshooting

### Common Issues

1. **API Not Running**:
   ```
   ❌ API not available: Connection refused
   ```
   **Solution**: Start the API server first

2. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'app'
   ```
   **Solution**: Run from project root or add to Python path

3. **Timeout Errors**:
   ```
   httpx.TimeoutException
   ```
   **Solution**: Increase timeout or check API performance

4. **Validation Errors**:
   ```
   HTTPStatusError: 422 Unprocessable Entity
   ```
   **Solution**: Check request data format

### Debug Mode

Run with debug information:

```bash
# Enable debug logging
PYTHONPATH=. python examples/run_tests.py --test-type tests

# Run with verbose output
python -u examples/run_tests.py
```

### API Debug Mode

Start API in debug mode:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## 📈 Monitoring

### Health Checks

The examples include health checks:

```python
# Check API health
health = await client.health_check()
print(f"API Status: {health['status']}")
```

### Performance Monitoring

Monitor performance during tests:

```python
# Time operations
start_time = time.time()
# ... perform operation ...
end_time = time.time()
print(f"Operation took {end_time - start_time:.2f} seconds")
```

### Memory Usage

Monitor memory usage:

```python
import psutil
import os

# Get memory usage
process = psutil.Process(os.getpid())
memory_mb = process.memory_info().rss / 1024 / 1024
print(f"Memory usage: {memory_mb:.2f} MB")
```

## 🎯 Best Practices

### 1. Test Organization
- Group related tests together
- Use descriptive test names
- Include setup and teardown
- Test both success and failure cases

### 2. Error Handling
- Always handle exceptions
- Provide meaningful error messages
- Test error scenarios
- Validate error responses

### 3. Performance Testing
- Test with realistic data sizes
- Measure multiple metrics
- Test under load
- Monitor resource usage

### 4. Data Management
- Clean up test data
- Use unique identifiers
- Avoid data conflicts
- Test data consistency

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **System Design**: ../SYSTEM_DESIGN.md
- **Main README**: ../README.md
- **Configuration**: ../app/config.py

## 🤝 Contributing

To add new examples or tests:

1. Create new example files in this directory
2. Follow the existing naming conventions
3. Include comprehensive documentation
4. Add error handling
5. Test your examples thoroughly

## 📄 License

This project is part of the Stack AI take-home assignment.
