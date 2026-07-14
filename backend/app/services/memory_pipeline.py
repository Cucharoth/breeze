import json
from app.repositories.kg_repository import kg_repository
from app.services.llm_service import LLMService
from app.core.logger import logger
from app.core.prompt_manager import format_prompt

from typing import List
from app.models.message import Message

async def extract_knowledge(branch_id: str, messages: List[Message], llm_service: LLMService):
    """Asynchronous task to extract entities and relationships from a batch of messages."""
    logger.info(f"Starting knowledge extraction for branch {branch_id} (batch size: {len(messages)})...")
    
    # Format the batch of messages into a single text block
    content = "\n".join([f"{m.role}: {m.content}" for m in messages])
    prompt = format_prompt("knowledge_extractor", content=content)
    
    try:
        from app.core.database import AsyncSessionLocal
        from app.services.kg_service import kg_service
        
        # Use generate_json to ensure valid extraction
        data = await llm_service.generate_json(prompt)
        if not data:
            logger.warning("Empty JSON returned from LLM extraction")
            return
            
        async with AsyncSessionLocal() as db:
            for entity in data.get("entities", []):
                name = entity.get("name")
                if not name:
                    continue
                    
                node_type = entity.get("type", "unknown")
                description = entity.get("description", "")
                
                # Generate embedding
                emb_text = f"{name} ({node_type}): {description}"
                embedding_vector = await kg_service.generate_embedding(emb_text)
                
                node = await kg_repository.add_node(
                    db, 
                    branch_id=branch_id, 
                    name=name, 
                    node_type=node_type, 
                    description=description
                )
                
                if embedding_vector:
                    node.embedding = json.dumps(embedding_vector)
            
            await db.commit()
            logger.info(f"Knowledge extraction complete for branch {branch_id} (batch size: {len(messages)})")
            
    except Exception as e:
        logger.error(f"Knowledge extraction failed: {e}")
