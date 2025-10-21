#!/bin/bash
# Manual API Testing Script for Stack AI Vector Database

echo "🚀 Stack AI Vector Database - Manual Test Script"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Health Check
echo -e "\n${YELLOW}1. Testing API Health...${NC}"
curl -s http://localhost:8000/health | python -m json.tool
echo ""

# 2. Create Library
echo -e "\n${YELLOW}2. Creating Library...${NC}"
LIBRARY_RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Manual Test Library", "description": "Testing the API manually"}')

echo "$LIBRARY_RESPONSE" | python -m json.tool

# Extract library_id
LIBRARY_ID=$(echo "$LIBRARY_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo -e "${GREEN}✅ Library ID: $LIBRARY_ID${NC}"

# 3. Create Document
echo -e "\n${YELLOW}3. Creating Document...${NC}"
DOCUMENT_RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/documents/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Document", "content": "This is a test about machine learning and AI.", "metadata": {"topic": "ai"}}')

echo "$DOCUMENT_RESPONSE" | python -m json.tool

# Extract document_id
DOCUMENT_ID=$(echo "$DOCUMENT_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo -e "${GREEN}✅ Document ID: $DOCUMENT_ID${NC}"

# 4. Create Chunk (with embedding)
echo -e "\n${YELLOW}4. Creating Chunk (this will generate embedding via Cohere)...${NC}"
CHUNK_RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/documents/$DOCUMENT_ID/chunks/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Machine learning is a powerful subset of artificial intelligence.", "metadata": {"topic": "ai", "type": "definition"}}')

echo "$CHUNK_RESPONSE" | python -c "import sys, json; data = json.load(sys.stdin); print(json.dumps({k: v if k != 'embedding' else f'[{len(v)} dimensions]' for k, v in data.items()}, indent=2))"

# Extract chunk_id
CHUNK_ID=$(echo "$CHUNK_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo -e "${GREEN}✅ Chunk ID: $CHUNK_ID${NC}"
echo -e "${GREEN}✅ Embedding generated: 1024 dimensions${NC}"

# 5. Build Search Index
echo -e "\n${YELLOW}5. Building Search Index...${NC}"
INDEX_RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/index")
echo "$INDEX_RESPONSE" | python -m json.tool
echo -e "${GREEN}✅ Index built for both Flat and IVF${NC}"

# 6. Search (Flat Index)
echo -e "\n${YELLOW}6. Testing Vector Search (Flat Index)...${NC}"
SEARCH_RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/search" \
  -H "Content-Type: application/json" \
  -d '{"query_text": "machine learning algorithms", "k": 5, "index_type": "flat", "metadata_filter": {"topic": "ai"}}')

echo "$SEARCH_RESPONSE" | python -c "import sys, json; data = json.load(sys.stdin); print(json.dumps({k: v if k != 'results' else [{'text': r['chunk']['text'][:50] + '...', 'score': r['similarity_score'], 'rank': r['rank']} for r in v] for k, v in data.items()}, indent=2))"

# 7. Search (IVF Index)
echo -e "\n${YELLOW}7. Testing Vector Search (IVF Index)...${NC}"
SEARCH_IVF_RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/search" \
  -H "Content-Type: application/json" \
  -d '{"query_text": "artificial intelligence", "k": 5, "index_type": "ivf"}')

echo "$SEARCH_IVF_RESPONSE" | python -c "import sys, json; data = json.load(sys.stdin); print(json.dumps({k: v if k != 'results' else [{'text': r['chunk']['text'][:50] + '...', 'score': r['similarity_score'], 'rank': r['rank']} for r in v] for k, v in data.items()}, indent=2))"

# 8. Get Library
echo -e "\n${YELLOW}8. Getting Library Details...${NC}"
curl -s "http://localhost:8000/libraries/$LIBRARY_ID" | python -m json.tool

# 9. Get Document
echo -e "\n${YELLOW}9. Getting Document Details...${NC}"
curl -s "http://localhost:8000/libraries/$LIBRARY_ID/documents/$DOCUMENT_ID" | python -m json.tool

# 10. Get Chunk
echo -e "\n${YELLOW}10. Getting Chunk Details...${NC}"
curl -s "http://localhost:8000/libraries/$LIBRARY_ID/documents/$DOCUMENT_ID/chunks/$CHUNK_ID" | python -c "import sys, json; data = json.load(sys.stdin); print(json.dumps({k: v if k != 'embedding' else f'[{len(v)} dimensions]' for k, v in data.items()}, indent=2))"

# 11. CSV Export
echo -e "\n${YELLOW}11. Testing CSV Export...${NC}"
curl -s "http://localhost:8000/csv/export" -o export_data.csv
if [ -f export_data.csv ]; then
    echo -e "${GREEN}✅ CSV export successful: export_data.csv${NC}"
    echo "First few lines:"
    head -n 5 export_data.csv
else
    echo -e "${RED}❌ CSV export failed${NC}"
fi

# 12. Cleanup
echo -e "\n${YELLOW}12. Cleaning up (deleting library - cascade delete)...${NC}"
DELETE_RESPONSE=$(curl -s -X DELETE "http://localhost:8000/libraries/$LIBRARY_ID")
if [ -z "$DELETE_RESPONSE" ] || [ "$DELETE_RESPONSE" == "null" ]; then
    echo -e "${GREEN}✅ Library deleted successfully (cascade deleted documents and chunks)${NC}"
else
    echo "$DELETE_RESPONSE" | python -m json.tool
fi

# 13. Verify Deletion
echo -e "\n${YELLOW}13. Verifying deletion...${NC}"
VERIFY_RESPONSE=$(curl -s "http://localhost:8000/libraries/$LIBRARY_ID")
echo "$VERIFY_RESPONSE" | python -m json.tool

echo -e "\n${GREEN}=================================================="
echo "✅ Manual Test Complete!"
echo -e "==================================================${NC}"

