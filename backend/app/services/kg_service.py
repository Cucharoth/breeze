import json
import math
import httpx
from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.kg_repository import kg_repository
from app.models.kg_node import KGNode
from app.core.logger import logger

class KGService:
    def __init__(self):
        # We assume Ollama is running locally on the standard port, as used by llm_service
        self.ollama_url = "http://localhost:11434/api/embeddings"
        self.embedding_model = "nomic-embed-text"

    async def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding vector using Ollama."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.ollama_url,
                    json={
                        "model": self.embedding_model,
                        "prompt": text
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("embedding", [])
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            return []

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors in pure Python."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = math.sqrt(sum(a * a for a in vec1))
        norm_b = math.sqrt(sum(b * b for b in vec2))

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)

    async def get_relevant_context(
        self, 
        db: AsyncSession, 
        branch_id: str, 
        user_message: str,
        top_k: int = 3
    ) -> str:
        """
        Embeds the user message, calculates similarities against all branch nodes,
        and returns a formatted context string of the most relevant nodes.
        """
        nodes = await kg_repository.get_nodes(db, branch_id)
        if not nodes:
            return ""

        user_embedding = await self.generate_embedding(user_message)
        if not user_embedding:
            return ""

        scored_nodes: List[Tuple[float, KGNode]] = []
        dirty_nodes = False

        for node in nodes:
            node_emb = None
            if node.embedding:
                try:
                    node_emb = json.loads(node.embedding)
                except Exception:
                    pass
            
            # If a node doesn't have an embedding yet (e.g. legacy data or extraction failure)
            if not node_emb:
                content_to_embed = f"{node.name} ({node.type}): {node.description}"
                node_emb = await self.generate_embedding(content_to_embed)
                if node_emb:
                    node.embedding = json.dumps(node_emb)
                    dirty_nodes = True
            
            if node_emb:
                sim = self.cosine_similarity(user_embedding, node_emb)
                scored_nodes.append((sim, node))

        # Commit any newly generated embeddings
        if dirty_nodes:
            await db.commit()

        # Sort by highest similarity
        scored_nodes.sort(key=lambda x: x[0], reverse=True)
        
        # Filter nodes above a reasonable similarity threshold (e.g., 0.5 for nomic)
        top_nodes = [node for sim, node in scored_nodes[:top_k] if sim > 0.4]

        if not top_nodes:
            return ""

        context_lines = ["\n\nRelevant Knowledge:"]
        for node in top_nodes:
            context_lines.append(f"- {node.name} ({node.type}): {node.description}")

        return "\n".join(context_lines)

kg_service = KGService()
