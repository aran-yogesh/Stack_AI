#!/bin/bash
# Setup script for Stack AI Vector Database

echo "🚀 Setting up Stack AI Vector Database..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check for Cohere API key
if [ -z "$COHERE_API_KEY" ]; then
    echo ""
    echo "⚠️  WARNING: COHERE_API_KEY environment variable not set!"
    echo "   Please set your Cohere API key:"
    echo "   export COHERE_API_KEY='your_api_key_here'"
    echo ""
    echo "   Or create a .env file with:"
    echo "   COHERE_API_KEY=your_api_key_here"
    echo ""
fi

echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  export COHERE_API_KEY='your_api_key_here'"
echo "  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "To test the system:"
echo "  python test_complete_system.py"
