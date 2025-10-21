# 🔑 How to Get IDs from API Responses

## 🎯 **Quick Answer:**

Use the helper script:

```bash
./get_library_id.sh
# Returns: Library ID: 96940979-682c-4a12-b079-43456bd79c04
```

---

## 📋 **Step-by-Step Guide:**

### **1. Create Library and Get ID**

```bash
# Create library
RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Library", "description": "Test"}')

# Extract ID
LIBRARY_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

# Use it
echo "Library ID: $LIBRARY_ID"
```

### **2. Create Document and Get ID**

```bash
# Create document (using LIBRARY_ID from above)
RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/documents/" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Doc", "content": "Content here"}')

# Extract ID
DOCUMENT_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo "Document ID: $DOCUMENT_ID"
```

### **3. Create Chunk and Get ID**

```bash
# Create chunk
RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/documents/$DOCUMENT_ID/chunks/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Some text here", "metadata": {"topic": "test"}}')

# Extract ID
CHUNK_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo "Chunk ID: $CHUNK_ID"
```

---

## 🚀 **Complete Workflow Example:**

```bash
# Step 1: Create Library
echo "Creating library..."
LIBRARY=$(curl -s -X POST "http://localhost:8000/libraries/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Library", "description": "Testing"}')
LIBRARY_ID=$(echo "$LIBRARY" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✅ Library ID: $LIBRARY_ID"

# Step 2: Create Document
echo "Creating document..."
DOCUMENT=$(curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/documents/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Doc 1", "content": "Machine learning content"}')
DOCUMENT_ID=$(echo "$DOCUMENT" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✅ Document ID: $DOCUMENT_ID"

# Step 3: Create Chunk
echo "Creating chunk..."
CHUNK=$(curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/documents/$DOCUMENT_ID/chunks/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Machine learning is powerful", "metadata": {"topic": "ai"}}')
CHUNK_ID=$(echo "$CHUNK" | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✅ Chunk ID: $CHUNK_ID"

# Step 4: Build Index
echo "Building search index..."
curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/index" | python -m json.tool

# Step 5: Search
echo "Searching..."
curl -s -X POST "http://localhost:8000/libraries/$LIBRARY_ID/search" \
  -H "Content-Type: application/json" \
  -d '{"query_text": "machine learning", "k": 5}' | python -m json.tool
```

---

## 💡 **Alternative Methods:**

### **Method 1: List All and Pick One**

```bash
# Get all libraries
curl -s "http://localhost:8000/libraries/" | python -m json.tool

# Copy an ID from the output
LIBRARY_ID="paste-id-here"
```

### **Method 2: Using jq (if installed)**

```bash
# Install jq: brew install jq

# Create and extract in one line
LIBRARY_ID=$(curl -s -X POST "http://localhost:8000/libraries/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "description": "Test"}' | jq -r '.id')

echo $LIBRARY_ID
```

### **Method 3: Save to File**

```bash
# Save response to file
curl -X POST "http://localhost:8000/libraries/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "description": "Test"}' > response.json

# View file
cat response.json | python -m json.tool

# Extract ID
LIBRARY_ID=$(cat response.json | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
```

---

## 🎯 **Pro Tips:**

### **Tip 1: Store IDs as Environment Variables**

```bash
# After creating, export for later use
export LIBRARY_ID="96940979-682c-4a12-b079-43456bd79c04"
export DOCUMENT_ID="06bb5d20-00ee-44a7-9f33-ec0654436455"

# Now you can use them anywhere in your terminal session
curl -X POST "http://localhost:8000/libraries/$LIBRARY_ID/index"
```

### **Tip 2: Create a Function**

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
get_library_id() {
    curl -s "http://localhost:8000/libraries/" | \
    python -c "import sys, json; libs = json.load(sys.stdin); print(libs[0]['id'] if libs else 'No libraries found')"
}

# Usage:
LIBRARY_ID=$(get_library_id)
```

### **Tip 3: Use the Automated Scripts**

```bash
# Best option - handles everything automatically!
./manual_test.sh
```

---

## 🔍 **Troubleshooting:**

### **Problem: Can't extract ID**

```bash
# Make sure the response is valid JSON first
RESPONSE=$(curl -s -X POST "http://localhost:8000/libraries/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "description": "Test"}')

# Check response
echo "$RESPONSE"

# If it's valid JSON, extract ID
echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['id'])"
```

### **Problem: ID not found in response**

```bash
# Check if the API returned an error
echo "$RESPONSE" | python -m json.tool

# Look for "id" field in the output
```

---

## ✅ **Summary:**

**Three Easy Ways to Get IDs:**

1. **🚀 Automated Script** (Easiest)
   ```bash
   ./get_library_id.sh
   ```

2. **📋 Extract from Response** (Most Common)
   ```bash
   ID=$(curl -s ... | python -c "import sys, json; print(json.load(sys.stdin)['id'])")
   ```

3. **📝 Copy-Paste** (Manual but Simple)
   ```bash
   curl ... | python -m json.tool
   # Copy the "id" value from output
   ```

**For your demo, use the automated scripts - they handle everything!** 🎉
