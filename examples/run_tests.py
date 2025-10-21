#!/usr/bin/env python3
"""
Simple Test Runner for Stack AI Vector Database

This script provides an easy way to run all the example tests and demonstrations.

Usage:
    python examples/run_tests.py [--test-type TYPE] [--help]

Test Types:
    - crud: Run CRUD examples
    - tests: Run comprehensive test suite
    - benchmark: Run performance benchmark
    - all: Run all tests (default)
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from examples.crud_examples import main as run_crud_examples
from examples.testing_examples import main as run_testing_examples
from examples.testing_examples import run_performance_benchmark


async def run_crud_demo():
    """Run CRUD examples demonstration."""
    print("🚀 Running CRUD Examples...")
    print("=" * 60)
    try:
        await run_crud_examples()
        print("✅ CRUD examples completed successfully!")
    except Exception as e:
        print(f"❌ CRUD examples failed: {e}")
        return False
    return True


async def run_test_suite():
    """Run comprehensive test suite."""
    print("🧪 Running Test Suite...")
    print("=" * 60)
    try:
        await run_testing_examples()
        print("✅ Test suite completed successfully!")
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        return False
    return True


async def run_benchmark():
    """Run performance benchmark."""
    print("📊 Running Performance Benchmark...")
    print("=" * 60)
    try:
        await run_performance_benchmark()
        print("✅ Performance benchmark completed successfully!")
    except Exception as e:
        print(f"❌ Performance benchmark failed: {e}")
        return False
    return True


async def check_api_health():
    """Check if the API is running and healthy."""
    import httpx
    
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


async def main():
    """Main function to run tests based on command line arguments."""
    parser = argparse.ArgumentParser(description="Run Stack AI Vector Database tests and examples")
    parser.add_argument(
        "--test-type",
        choices=["crud", "tests", "benchmark", "all"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "--skip-health-check",
        action="store_true",
        help="Skip API health check"
    )
    
    args = parser.parse_args()
    
    print("🧪 Stack AI Vector Database - Test Runner")
    print("=" * 60)
    
    # Check API health unless skipped
    if not args.skip_health_check:
        if not await check_api_health():
            return 1
    
    success = True
    
    # Run tests based on type
    if args.test_type in ["crud", "all"]:
        success &= await run_crud_demo()
        print()
    
    if args.test_type in ["tests", "all"]:
        success &= await run_test_suite()
        print()
    
    if args.test_type in ["benchmark", "all"]:
        success &= await run_benchmark()
        print()
    
    # Summary
    if success:
        print("🎉 All tests completed successfully!")
        return 0
    else:
        print("❌ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
