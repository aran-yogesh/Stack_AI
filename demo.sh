#!/bin/bash
# Demo script for Stack AI Vector Database

echo "🚀 Stack AI Vector Database Demo"
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first:"
    echo "   ./setup.sh"
    exit 1
fi

# Check for Cohere API key
if [ -z "$COHERE_API_KEY" ]; then
    echo "❌ COHERE_API_KEY environment variable not set!"
    echo "   Please set your Cohere API key:"
    echo "   export COHERE_API_KEY='your_api_key_here'"
    exit 1
fi

echo "✅ Environment check passed"
echo ""

# Start the server in background
echo "🔧 Starting FastAPI server..."
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Test the system
echo "🧪 Running system tests..."
python test_complete_system.py

echo ""
echo "🎉 Demo complete!"
echo ""
echo "📚 API Documentation:"
echo "   Swagger UI: http://localhost:8000/docs"
echo "   ReDoc: http://localhost:8000/redoc"
echo ""
echo "🔍 Test endpoints:"
echo "   Health: curl http://localhost:8000/health"
echo "   Root: curl http://localhost:8000/"
echo ""
echo "🛑 To stop the server: kill $SERVER_PID"
