#!/usr/bin/env python3
"""Complete system test for Stack AI Vector Database."""

import asyncio

import httpx


async def test_api_health():
    """Test API health endpoint."""
    print("🔍 Testing API Health...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✅ API is healthy")
                return True
            else:
                print(f"❌ API health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ API health check error: {e}")
        return False


async def test_core_crud():
    """Test core CRUD operations."""
    print("\n🔧 Testing Core CRUD Operations...")
    
    try:
        async with httpx.AsyncClient() as client:
            # Test 1: Create Library
            print("   📚 Creating library...")
            library_data = {
                "name": "Test Library",
                "description": "A test library for system testing"
            }
            response = await client.post("http://localhost:8000/libraries/", json=library_data)
            if response.status_code != 201:
                print(f"❌ Library creation failed: {response.status_code}")
                return False
            
            library = response.json()
            library_id = library["id"]
            print(f"   ✅ Created library: {library_id}")
            
            # Test 2: Create Document
            print("   📄 Creating document...")
            document_data = {
                "title": "Test Document",
                "content": "This is a test document about machine learning and artificial intelligence.",
                "metadata": {"topic": "ai", "test": True}
            }
            response = await client.post(
                f"http://localhost:8000/libraries/{library_id}/documents/",
                json=document_data
            )
            if response.status_code != 201:
                print(f"❌ Document creation failed: {response.status_code}")
                return False
            
            document = response.json()
            document_id = document["id"]
            print(f"   ✅ Created document: {document_id}")
            
            # Test 3: Create Chunk
            print("   📝 Creating chunk...")
            chunk_data = {
                "text": "Machine learning is a subset of artificial intelligence that focuses on algorithms.",
                "metadata": {"topic": "ai", "test": True}
            }
            response = await client.post(
                f"http://localhost:8000/libraries/{library_id}/documents/{document_id}/chunks/",
                json=chunk_data
            )
            if response.status_code != 201:
                print(f"❌ Chunk creation failed: {response.status_code}")
                return False
            
            chunk = response.json()
            chunk_id = chunk["id"]
            print(f"   ✅ Created chunk: {chunk_id}")
            
            # Test 4: Build Index
            print("   🔨 Building search index...")
            response = await client.post(f"http://localhost:8000/libraries/{library_id}/index")
            if response.status_code not in [200, 202]:
                print(f"❌ Index building failed: {response.status_code}")
                return False
            
            index_stats = response.json()
            print(f"   ✅ Index built successfully")
            
            # Test 5: Search
            print("   🔍 Testing search...")
            search_data = {
                "query_text": "machine learning",
                "k": 5,
                "metadata_filter": {"topic": "ai"}
            }
            response = await client.post(
                f"http://localhost:8000/libraries/{library_id}/search",
                json=search_data
            )
            if response.status_code != 200:
                print(f"❌ Search failed: {response.status_code}")
                return False
            
            search_results = response.json()
            print(f"   ✅ Search successful: {len(search_results['results'])} results")
            
            # Test 6: Cleanup
            print("   🗑️ Cleaning up...")
            response = await client.delete(f"http://localhost:8000/libraries/{library_id}")
            if response.status_code != 200:
                print(f"⚠️ Cleanup failed: {response.status_code}")
            else:
                print("   ✅ Cleanup successful")
            
            return True
            
    except Exception as e:
        print(f"❌ CRUD test failed: {e}")
        return False


async def main():
    """Run all tests."""
    print("🚀 Stack AI Vector Database - Complete System Test")
    print("=" * 60)
    
    # Test API health
    health_ok = await test_api_health()
    
    # Test core CRUD operations
    crud_ok = await test_core_crud()
    
    # Print results
    print("\n" + "=" * 60)
    print("🏁 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"✅ API Health: {'PASS' if health_ok else 'FAIL'}")
    print(f"✅ Core CRUD: {'PASS' if crud_ok else 'FAIL'}")
    
    if health_ok and crud_ok:
        print("\n🎉 ALL TESTS PASSED! The Vector Database is working perfectly!")
        print("✅ Core functionality: Working")
        print("✅ Ready for Stack AI submission!")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())