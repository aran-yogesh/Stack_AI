"""Configuration settings for the Vector Database application."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    app_name: str = "Vector Database API"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Cohere API Configuration - MUST be provided via environment variable
    cohere_api_key: str  # Required - no default for security
    cohere_model: str = "embed-english-v3.0"
    
    # Vector Configuration
    embedding_dimension: int = 1024  # Cohere embed-english-v3.0 dimension
    max_chunk_size: int = 1000
    default_k: int = 10  # Default number of results for k-NN search
    
    # Indexing Configuration
    ivf_n_clusters: int = 100  # Number of clusters for IVF index
    ivf_max_iterations: int = 100  # Max iterations for K-Means
    
    # Concurrency Configuration
    max_concurrent_operations: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
