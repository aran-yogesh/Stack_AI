#!/usr/bin/env python3
"""
Simple Test Runner for Stack AI Vector Database

This script provides an easy way to run basic tests and examples.

Usage:
    python examples/simple_test_runner.py
"""

import asyncio
import sys
from pathlib import Path

import httpx

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def check_api_health():
    """Check if the API is running and healthy."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ API is healthy: {health_data['status']}")
                return True
            else:
                print(f"❌ API health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ API not available: {e}")
        print("Please start the API server first:")
        print("  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        return False


async def run_simple_crud_example():
    """Run the simple CRUD example."""
    print("\n🚀 Running Simple CRUD Example...")
    print("=" * 50)

    try:
        from examples.simple_crud_example import main as run_crud
        await run_crud()
        print("✅ Simple CRUD example completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Simple CRUD example failed: {e}")
        return False


async def run_basic_tests():
    """Run basic API tests."""
    print("\n🧪 Running Basic API Tests...")
    print("=" * 50)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test root endpoint
            print("1. Testing root endpoint...")
            response = await client.get("http://localhost:8000/")
            assert response.status_code == 200
            root_data = response.json()
            assert 'message' in root_data
            print("   ✅ Root endpoint working")

            # Test health endpoint
            print("2. Testing health endpoint...")
            response = await client.get("http://localhost:8000/health")
            assert response.status_code == 200
            health_data = response.json()
            assert health_data['status'] == 'healthy'
            print("   ✅ Health endpoint working")

            # Test library creation
            print("3. Testing library creation...")
            library_data = {
                "name": "Test Library",
                "description": "A test library for basic testing"
            }
            response = await client.post("http://localhost:8000/libraries/", json=library_data)
            assert response.status_code == 201
            library = response.json()
            assert library['name'] == library_data['name']
            print(f"   ✅ Created library: {library['name']}")

            # Test document creation
            print("4. Testing document creation...")
            document_data = {
                "title": "Test Document",
                "content": "This is a test document for basic testing."
            }
            response = await client.post(
                f"http://localhost:8000/libraries/{library['id']}/documents/",
                json=document_data
            )
            assert response.status_code == 201
            document = response.json()
            assert document['title'] == document_data['title']
            print(f"   ✅ Created document: {document['title']}")

            # Test chunk creation
            print("5. Testing chunk creation...")
            chunk_data = {
                "text": "This is a test chunk for basic testing."
            }
            response = await client.post(
                f"http://localhost:8000/libraries/{library['id']}/documents/{document['id']}/chunks/",
                json=chunk_data
            )
            assert response.status_code == 201
            chunk = response.json()
            assert chunk['text'] == chunk_data['text']
            print(f"   ✅ Created chunk: {chunk['text'][:50]}...")

            # Test index building
            print("6. Testing index building...")
            response = await client.post(f"http://localhost:8000/libraries/{library['id']}/index")
            assert response.status_code == 200
            print("   ✅ Index built successfully")

            # Wait for indexing
            await asyncio.sleep(2)

            # Test search
            print("7. Testing search...")
            search_data = {
                "query_text": "test chunk",
                "k": 5
            }
            response = await client.post(
                f"http://localhost:8000/libraries/{library['id']}/search",
                json=search_data
            )
            assert response.status_code == 200
            search_results = response.json()
            assert 'results' in search_results
            assert 'total_results' in search_results
            print(f"   ✅ Search working: {search_results['total_results']} results")

            # Cleanup
            print("8. Cleaning up...")
            response = await client.delete(f"http://localhost:8000/libraries/{library['id']}")
            assert response.status_code == 204
            print("   ✅ Cleanup completed")

        print("\n✅ All basic tests passed!")
        return True

    except Exception as e:
        print(f"\n❌ Basic tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main function to run all tests."""
    print("🧪 Stack AI Vector Database - Simple Test Runner")
    print("=" * 60)

    # Check API health
    if not await check_api_health():
        return 1

    success = True

    # Run basic tests
    success &= await run_basic_tests()

    # Run simple CRUD example
    success &= await run_simple_crud_example()

    # Summary
    if success:
        print("\n🎉 All tests completed successfully!")
        print("=" * 60)
        return 0
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
