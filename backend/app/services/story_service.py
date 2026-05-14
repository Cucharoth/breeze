from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.story_repository import story_repository
from app.repositories.branch_repository import branch_repository
from app.repositories.message_repository import message_repository
from app.repositories.checkpoint_repository import checkpoint_repository
from app.repositories.scenario_repository import scenario_repository
from app.repositories.summary_repository import summary_repository
from app.services.llm.base import LLMAdapter
from app.models.story import Story
from app.models.branch import Branch
from app.models.message import Message
from app.models.checkpoint import Checkpoint
from typing import List

class StoryService:
    async def create_story(self, db: AsyncSession, scenario_id: int) -> Story:
        story = await story_repository.create(db, obj_in_data={"scenario_id": scenario_id})
        main_branch = await branch_repository.create(
            db, 
            obj_in_data={"story_id": story.id, "name": "Main Branch"}
        )
        
        scenario = await scenario_repository.get(db, scenario_id)
        if scenario:
             await message_repository.create(
                db, 
                obj_in_data={
                    "branch_id": main_branch.id,
                    "role": "system",
                    "content": scenario.first_scene
                }
            )
        
        story.main_branch_id = main_branch.id
        return story

    async def add_message(self, db: AsyncSession, branch_id: int, role: str, content: str) -> Message:
        return await message_repository.create(
            db, 
            obj_in_data={"branch_id": branch_id, "role": role, "content": content}
        )

    async def create_checkpoint(self, db: AsyncSession, branch_id: int, message_id: int) -> Checkpoint:
        return await checkpoint_repository.create(
            db, 
            obj_in_data={"branch_id": branch_id, "message_id": message_id}
        )

    async def spawn_branch(self, db: AsyncSession, checkpoint_id: int, name: str) -> Branch:
        checkpoint = await checkpoint_repository.get(db, checkpoint_id)
        if not checkpoint:
            raise ValueError("Checkpoint not found")
            
        parent_branch = await branch_repository.get(db, checkpoint.branch_id)
        return await branch_repository.create(
            db, 
            obj_in_data={
                "story_id": parent_branch.story_id,
                "parent_checkpoint_id": checkpoint_id,
                "name": name
            }
        )

    async def get_history(self, db: AsyncSession, branch_id: int) -> List[Message]:
        history = []
        curr_branch_id = branch_id
        limit_message_id = None
        
        while curr_branch_id:
            # Query messages for current branch
            query = select(Message).where(Message.branch_id == curr_branch_id)
            
            # If we have a limit (from a checkpoint), filter by it
            if limit_message_id:
                # We want messages up to and including the checkpoint message
                # Since messages are created sequentially, we can use ID or a more robust order
                query = query.where(Message.id <= limit_message_id)
            
            query = query.order_by(Message.created_at.desc())
            result = await db.execute(query)
            branch_msgs = list(result.scalars().all())
            
            # Add to history (prepend since we are walking backwards)
            history = branch_msgs + history
            
            # Move to parent
            branch = await branch_repository.get(db, curr_branch_id)
            if branch and branch.parent_checkpoint_id:
                checkpoint = await checkpoint_repository.get(db, branch.parent_checkpoint_id)
                curr_branch_id = checkpoint.branch_id
                limit_message_id = checkpoint.message_id
            else:
                curr_branch_id = None
                
        # Final sort by creation time
        history.sort(key=lambda x: x.created_at)
        return history

    async def generate_summary(self, db: AsyncSession, branch_id: int, adapter: LLMAdapter) -> str:
        # Get history
        history = await self.get_history(db, branch_id)
        if len(history) < 2:
            return "No history to summarize"
            
        # For simplicity, summarize everything currently in history
        text_to_summarize = "\n".join([f"{m.role}: {m.content}" for m in history])
        prompt = f"Summarize this roleplay history:\n{text_to_summarize}"
        
        summary_content = await adapter.generate(prompt)
        
        # Save to DB
        await summary_repository.create(db, obj_in_data={
            "branch_id": branch_id,
            "last_message_id": history[-1].id,
            "content": summary_content
        })
        
        return summary_content

story_service = StoryService()
