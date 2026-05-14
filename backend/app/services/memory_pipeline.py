import json
from app.repositories.kg_repository import kg_repository
from app.services.llm_service import LLMService
from app.core.logger import logger

async def extract_knowledge(branch_id: int, content: str, llm_service: LLMService):
    """Asynchronous task to extract entities and relationships."""
    prompt = f"""
    Extract entities (Characters, Locations, Objects, Events) and their relationships from the following text.
    Return ONLY a JSON object with this format:
    {{
        "entities": [{{ "name": "...", "type": "...", "description": "..." }}],
        "relationships": [{{ "source": "...", "target": "...", "relationship": "..." }}]
    }}
    Text: {content}
    """
    
    try:
        from app.core.database import AsyncSessionLocal
        response_text = await llm_service.generate_text(prompt)
        # Simple extraction (find the first { and last })
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start == -1 or end == 0:
            logger.warning("No valid JSON found in LLM extraction response")
            return

        data = json.loads(response_text[start:end])
        
        async with AsyncSessionLocal() as db:
            for entity in data.get("entities", []):
                await kg_repository.add_node(
                    db, 
                    branch_id=branch_id, 
                    name=entity["name"], 
                    node_type=entity["type"], 
                    description=entity.get("description")
                )
            
            # (Future: Handle relationships mapping names to node IDs)
            
            await db.commit()
            logger.info(f"Knowledge extraction complete for branch {branch_id}")
            
    except Exception as e:
        logger.error(f"Knowledge extraction failed: {e}")
