#!/bin/bash
# Simple script to create a library and get its ID

echo "🚀 Creating Library and Getting ID..."
echo ""

# Create library
RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Demo Library", "description": "Getting the library ID"}')

# Show full response
echo "Full Response:"
echo "$RESPONSE" | python -m json.tool
echo ""

# Extract and display just the ID
LIBRARY_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Library ID: $LIBRARY_ID"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Save to environment variable
echo "💡 To use this ID, copy-paste:"
echo "   export LIBRARY_ID=\"$LIBRARY_ID\""
echo ""
echo "Then you can use it like:"
echo "   curl -X POST \"http://localhost:8000/libraries/\$LIBRARY_ID/index\""

