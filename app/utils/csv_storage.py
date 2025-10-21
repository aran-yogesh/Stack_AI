"""CSV storage utility for embeddings and data visualization."""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from uuid import UUID

from app.models import Chunk, Document, Library


class CSVStorage:
    """Utility class for storing data in CSV format for visualization."""
    
    def __init__(self, base_dir: str = "data"):
        """Initialize CSV storage."""
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def save_libraries(self, libraries: List[Library]) -> str:
        """Save libraries to CSV."""
        filename = self.base_dir / f"libraries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'description', 'created_at', 'updated_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for library in libraries:
                writer.writerow({
                    'id': str(library.id),
                    'name': library.name,
                    'description': library.description,
                    'created_at': library.created_at.isoformat(),
                    'updated_at': library.updated_at.isoformat()
                })
        
        return str(filename)
    
    def save_documents(self, documents: List[Document]) -> str:
        """Save documents to CSV."""
        filename = self.base_dir / f"documents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'content', 'library_id', 'created_at', 'updated_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for document in documents:
                writer.writerow({
                    'id': str(document.id),
                    'title': document.title,
                    'content': document.content,
                    'library_id': str(document.library_id),
                    'created_at': document.created_at.isoformat(),
                    'updated_at': document.updated_at.isoformat()
                })
        
        return str(filename)
    
    def save_chunks_with_embeddings(self, chunks: List[Chunk]) -> str:
        """Save chunks with embeddings to CSV."""
        filename = self.base_dir / f"chunks_embeddings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'id', 'text', 'document_id', 'metadata', 'created_at', 'updated_at',
                'embedding_dimension', 'embedding_first_10', 'embedding_last_10'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for chunk in chunks:
                embedding = chunk.embedding
                writer.writerow({
                    'id': str(chunk.id),
                    'text': chunk.text,
                    'document_id': str(chunk.document_id),
                    'metadata': json.dumps(chunk.metadata),
                    'created_at': chunk.created_at.isoformat(),
                    'updated_at': chunk.updated_at.isoformat(),
                    'embedding_dimension': len(embedding),
                    'embedding_first_10': json.dumps(embedding[:10]),
                    'embedding_last_10': json.dumps(embedding[-10:])
                })
        
        return str(filename)
    
    def save_full_embeddings(self, chunks: List[Chunk]) -> str:
        """Save full embeddings to CSV (one row per chunk, columns for each dimension)."""
        if not chunks:
            return ""
        
        filename = self.base_dir / f"full_embeddings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Get embedding dimension from first chunk
        embedding_dim = len(chunks[0].embedding)
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Create fieldnames: id, text, metadata, then embedding dimensions
            fieldnames = ['id', 'text', 'metadata'] + [f'embedding_{i}' for i in range(embedding_dim)]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for chunk in chunks:
                row = {
                    'id': str(chunk.id),
                    'text': chunk.text,
                    'metadata': json.dumps(chunk.metadata)
                }
                # Add each embedding dimension as a separate column
                for i, value in enumerate(chunk.embedding):
                    row[f'embedding_{i}'] = value
                
                writer.writerow(row)
        
        return str(filename)
    
    def save_search_results(self, query: str, results: List[Dict[str, Any]], search_time_ms: float) -> str:
        """Save search results to CSV."""
        filename = self.base_dir / f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'query', 'chunk_id', 'text', 'similarity_score', 'rank', 
                'metadata', 'search_time_ms'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for i, result in enumerate(results):
                writer.writerow({
                    'query': query,
                    'chunk_id': str(result['chunk'].id),
                    'text': result['chunk'].text,
                    'similarity_score': result['similarity_score'],
                    'rank': i + 1,
                    'metadata': json.dumps(result['chunk'].metadata),
                    'search_time_ms': search_time_ms
                })
        
        return str(filename)
    
    def create_summary_report(self, libraries: List[Library], documents: List[Document], chunks: List[Chunk]) -> str:
        """Create a summary report."""
        filename = self.base_dir / f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Vector Database Summary Report\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            f.write(f"Libraries: {len(libraries)}\n")
            for lib in libraries:
                f.write(f"  - {lib.name}: {lib.description}\n")
            
            f.write(f"\nDocuments: {len(documents)}\n")
            for doc in documents:
                f.write(f"  - {doc.title}\n")
            
            f.write(f"\nChunks: {len(chunks)}\n")
            total_text_length = sum(len(chunk.text) for chunk in chunks)
            f.write(f"  - Total text length: {total_text_length} characters\n")
            
            if chunks:
                embedding_dim = len(chunks[0].embedding)
                f.write(f"  - Embedding dimension: {embedding_dim}\n")
                f.write(f"  - Total embeddings: {len(chunks)}\n")
            
            f.write(f"\nSample Chunks:\n")
            for i, chunk in enumerate(chunks[:5]):  # Show first 5 chunks
                f.write(f"  {i+1}. {chunk.text[:100]}...\n")
                f.write(f"     Embedding: [{chunk.embedding[0]:.4f}, {chunk.embedding[1]:.4f}, ...]\n")
        
        return str(filename)


# Global CSV storage instance
csv_storage = CSVStorage()
