#!/usr/bin/env python3
"""
Setup Script for Stack AI Vector Database Examples

This script helps set up the environment and run the examples.

Usage:
    python examples/setup_examples.py [--install-deps] [--start-api] [--run-examples]
"""

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "httpx",
        "numpy",
        "cohere",
        "pytest"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    return missing_packages


def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, cwd=Path(__file__).parent.parent)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def check_api_running():
    """Check if the API is running."""
    import httpx
    
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✅ API is running and healthy")
                return True
            else:
                print(f"❌ API is running but not healthy: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ API is not running: {e}")
        return False


def start_api():
    """Start the API server."""
    print("🚀 Starting API server...")
    
    try:
        # Start the API server in the background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "app.main:app",
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], cwd=Path(__file__).parent.parent)
        
        print("✅ API server started")
        print("   URL: http://localhost:8000")
        print("   Docs: http://localhost:8000/docs")
        print("   Health: http://localhost:8000/health")
        print("   Press Ctrl+C to stop the server")
        
        return process
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        return None


async def run_examples():
    """Run the examples."""
    print("🧪 Running examples...")
    
    try:
        # Import and run the examples
        from examples.run_tests import main as run_tests
        await run_tests()
        print("✅ Examples completed successfully")
        return True
    except Exception as e:
        print(f"❌ Examples failed: {e}")
        return False


def create_env_file():
    """Create a .env file if it doesn't exist."""
    env_file = Path(__file__).parent.parent / ".env"
    
    if not env_file.exists():
        print("📝 Creating .env file...")
        
        env_content = """# Stack AI Vector Database Configuration

# Cohere API Configuration
COHERE_API_KEY=your_cohere_api_key_here

# API Configuration
DEBUG=False
HOST=0.0.0.0
PORT=8000

# Vector Configuration
EMBEDDING_DIMENSION=1024
MAX_CHUNK_SIZE=1000
DEFAULT_K=10

# Indexing Configuration
IVF_N_CLUSTERS=100
IVF_MAX_ITERATIONS=100

# Concurrency Configuration
MAX_CONCURRENT_OPERATIONS=10
"""
        
        with open(env_file, "w") as f:
            f.write(env_content)
        
        print("✅ .env file created")
        print("⚠️  Please update COHERE_API_KEY in .env file")
    else:
        print("✅ .env file already exists")


def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description="Setup Stack AI Vector Database Examples")
    parser.add_argument("--install-deps", action="store_true", help="Install dependencies")
    parser.add_argument("--start-api", action="store_true", help="Start API server")
    parser.add_argument("--run-examples", action="store_true", help="Run examples")
    parser.add_argument("--all", action="store_true", help="Run all setup steps")
    
    args = parser.parse_args()
    
    print("🚀 Stack AI Vector Database - Setup Script")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check dependencies
    missing_packages = check_dependencies()
    
    # Install dependencies if requested or missing
    if args.install_deps or args.all or missing_packages:
        if missing_packages:
            print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        
        if not install_dependencies():
            return 1
    
    # Create .env file
    create_env_file()
    
    # Check if API is running
    api_running = check_api_running()
    
    # Start API if requested or not running
    if args.start_api or args.all or not api_running:
        if not api_running:
            process = start_api()
            if process is None:
                return 1
            
            # Wait a moment for the server to start
            import time
            time.sleep(3)
            
            # Check if it's running now
            if not check_api_running():
                print("❌ API failed to start properly")
                return 1
        else:
            print("✅ API is already running")
    
    # Run examples if requested
    if args.run_examples or args.all:
        print("\n" + "=" * 60)
        success = asyncio.run(run_examples())
        if not success:
            return 1
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Update COHERE_API_KEY in .env file")
    print("2. Start the API: python -m uvicorn app.main:app --reload")
    print("3. Run examples: python examples/run_tests.py")
    print("4. View API docs: http://localhost:8000/docs")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
