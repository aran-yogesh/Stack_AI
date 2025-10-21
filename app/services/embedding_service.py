"""Embedding service for converting text to vectors using Cohere API."""

import asyncio
from typing import List, Optional

import cohere

from app.config import settings


class EmbeddingService:
    """Service for generating embeddings using Cohere API."""
    
    def __init__(self):
        """Initialize the Cohere client."""
        self.client = cohere.Client(api_key=settings.cohere_api_key)
        self.model = settings.cohere_model
        self.dimension = settings.embedding_dimension
    
    async def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding vector
            
        Raises:
            ValueError: If text is empty or embedding generation fails
        """
        if not text.strip():
            raise ValueError("Text cannot be empty")
        
        try:
            # Run the synchronous Cohere call in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                self._get_embedding_sync, 
                text
            )
            return response
        except Exception as e:
            raise ValueError(f"Failed to generate embedding: {str(e)}")
    
    def _get_embedding_sync(self, text: str) -> List[float]:
        """Synchronous wrapper for Cohere embedding generation."""
        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type="search_document"
        )
        return response.embeddings[0]
    
    async def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            List of embedding vectors
            
        Raises:
            ValueError: If any text is empty or embedding generation fails
        """
        if not texts:
            return []
        
        # Filter out empty texts
        valid_texts = [text for text in texts if text.strip()]
        if not valid_texts:
            raise ValueError("No valid texts provided")
        
        try:
            # Run the synchronous Cohere call in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                self._get_embeddings_batch_sync, 
                valid_texts
            )
            return response
        except Exception as e:
            raise ValueError(f"Failed to generate embeddings: {str(e)}")
    
    def _get_embeddings_batch_sync(self, texts: List[str]) -> List[List[float]]:
        """Synchronous wrapper for batch Cohere embedding generation."""
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type="search_document"
        )
        return response.embeddings
    
    def get_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a search query.
        
        Args:
            query: Search query text
            
        Returns:
            List of floats representing the query embedding vector
            
        Raises:
            ValueError: If query is empty or embedding generation fails
        """
        if not query.strip():
            raise ValueError("Query cannot be empty")
        
        try:
            response = self.client.embed(
                texts=[query],
                model=self.model,
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            raise ValueError(f"Failed to generate query embedding: {str(e)}")


# Global embedding service instance
embedding_service = EmbeddingService()
