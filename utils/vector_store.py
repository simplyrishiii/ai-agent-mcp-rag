"""
Vector Store utilities for Pinecone integration
"""

import pinecone
from typing import List, Dict, Any, Tuple
import os

class VectorStore:
    def __init__(self, api_key: str, environment: str, index_name: str = "ai-agent-index"):
        """Initialize Pinecone vector store"""
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        
        # Initialize Pinecone
        pinecone.init(api_key=api_key, environment=environment)
        self.index = pinecone.Index(index_name)
    
    def upsert_vectors(
        self,
        vectors: List[Tuple[str, List[float], Dict[str, Any]]],
        namespace: str = ""
    ) -> Dict[str, Any]:
        """
        Upsert vectors to Pinecone
        
        Args:
            vectors: List of (id, embedding, metadata) tuples
            namespace: Optional namespace for grouping
        
        Returns:
            Upsert status
        """
        try:
            self.index.upsert(vectors=vectors, namespace=namespace)
            return {
                "status": "success",
                "count": len(vectors),
                "namespace": namespace
            }
        except Exception as e:
            raise Exception(f"Error upserting vectors: {str(e)}")
    
    def query_vectors(
        self,
        query_vector: List[float],
        top_k: int = 5,
        namespace: str = "",
        filter: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Query vectors from Pinecone
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            namespace: Optional namespace to search in
            filter: Optional metadata filter
        
        Returns:
            List of matching vectors with scores and metadata
        """
        try:
            results = self.index.query(
                vector=query_vector,
                top_k=top_k,
                namespace=namespace,
                filter=filter,
                include_metadata=True
            )
            
            return [
                {
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata
                }
                for match in results.matches
            ]
        except Exception as e:
            raise Exception(f"Error querying vectors: {str(e)}")
    
    def delete_vectors(self, ids: List[str], namespace: str = "") -> Dict[str, Any]:
        """Delete vectors by ID"""
        try:
            self.index.delete(ids=ids, namespace=namespace)
            return {
                "status": "success",
                "deleted_count": len(ids),
                "namespace": namespace
            }
        except Exception as e:
            raise Exception(f"Error deleting vectors: {str(e)}")
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": stats.namespaces
            }
        except Exception as e:
            raise Exception(f"Error getting index stats: {str(e)}")
    
    def create_index(self, dimension: int = 1536, metric: str = "cosine") -> Dict[str, Any]:
        """Create a new index in Pinecone"""
        try:
            pinecone.create_index(
                name=self.index_name,
                dimension=dimension,
                metric=metric
            )
            return {
                "status": "success",
                "index_name": self.index_name,
                "dimension": dimension,
                "metric": metric
            }
        except Exception as e:
            raise Exception(f"Error creating index: {str(e)}")