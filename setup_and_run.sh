#!/bin/bash

# Vector Database Setup Script
echo "🚀 Setting up Vector Database Backend..."

# Navigate to project directory
cd "/Users/aran/Desktop/stack ai"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install fastapi uvicorn pydantic pydantic-settings numpy cohere pytest pytest-asyncio httpx python-multipart

# Test import
echo "🧪 Testing imports..."
python3 -c "
try:
    import fastapi
    import uvicorn
    import pydantic
    import numpy
    import cohere
    print('✅ All dependencies imported successfully!')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

# Run the application
echo "🎯 Starting Vector Database API..."
echo "📖 API Documentation will be available at: http://localhost:8000/docs"
echo "🛑 Press Ctrl+C to stop the server"
uvicorn app.main:app --host 0.0.0.0 --port 8000
