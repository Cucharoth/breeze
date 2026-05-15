from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.story_repository import story_repository
from app.repositories.branch_repository import branch_repository
from app.repositories.message_repository import message_repository
from app.repositories.checkpoint_repository import checkpoint_repository
from app.repositories.scenario_repository import scenario_repository
from app.repositories.summary_repository import summary_repository
from app.services.llm_service import LLMService
from app.models.story import Story
from app.models.branch import Branch
from app.models.message import Message
from app.models.checkpoint import Checkpoint
from typing import List

class StoryService:
    async def create_story(self, db: AsyncSession, scenario_id: str) -> Story:
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

    async def add_message(self, db: AsyncSession, branch_id: str, role: str, content: str) -> Message:
        return await message_repository.create(
            db, 
            obj_in_data={"branch_id": branch_id, "role": role, "content": content}
        )

    async def create_checkpoint(self, db: AsyncSession, branch_id: str, message_id: str) -> Checkpoint:
        return await checkpoint_repository.create(
            db, 
            obj_in_data={"branch_id": branch_id, "message_id": message_id}
        )

    async def spawn_branch(self, db: AsyncSession, checkpoint_id: str, name: str) -> Branch:
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

    async def get_history(self, db: AsyncSession, branch_id: str) -> List[Message]:
        history = []
        curr_branch_id = branch_id
        limit_message_id = None
        
        while curr_branch_id:
            # Query messages for current branch
            query = select(Message).where(Message.branch_id == curr_branch_id)
            
            # If we have a limit (from a checkpoint), filter by it
            if limit_message_id:
                query = query.where(Message.id <= limit_message_id)
            
            query = query.order_by(Message.created_at.desc())
            result = await db.execute(query)
            branch_msgs = list(result.scalars().all())
            
            # Add to history
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

    async def generate_summary(self, db: AsyncSession, branch_id: str, llm_service: LLMService) -> str:
        history = await self.get_history(db, branch_id)
        if len(history) < 2:
            return "No history to summarize"
            
        text_to_summarize = "\n".join([f"{m.role}: {m.content}" for m in history])
        prompt = f"Summarize this roleplay history:\n{text_to_summarize}"
        
        summary_content = await llm_service.generate_text(prompt)
        
        await summary_repository.create(db, obj_in_data={
            "branch_id": branch_id,
            "last_message_id": history[-1].id,
            "content": summary_content
        })
        
        return summary_content

    async def generate_next_stream(self, db: AsyncSession, branch_id: str, llm_service: LLMService):
        """
        Generates the next GM message for a branch, streaming tokens.
        Includes branch-specific directives and history.
        """
        # 1. Fetch Context
        branch = await branch_repository.get(db, branch_id)
        if not branch:
            raise ValueError("Branch not found")
        
        story = await story_repository.get(db, branch.story_id)
        scenario = await scenario_repository.get(db, story.scenario_id) if story else None
        
        # 2. Fetch History
        history = await self.get_history(db, branch_id)
        
        # 3. Build System Prompt
        system_prompt = (
            "You are an expert Game Master for a deep, reactive roleplay experience. "
            "Write in the 2nd person ('You...') and focus on sensory details and consequences. "
            "Keep your responses concise and punchy—aim for 1 short paragraph, never exceed 15 words. "
            "Never speak for the player character."
        )
        
        if scenario:
            system_prompt += f"\n\nWorld Lore:\n{scenario.world_lore}"
            
        if branch.long_term_directive:
            system_prompt += f"\n\nLong-term Objective: {branch.long_term_directive}"
            
        if branch.short_term_directive:
            system_prompt += f"\n\nImmediate Goal: {branch.short_term_directive}"

        # 4. Build Conversation Prompt
        prompt = ""
        for msg in history:
            role_label = "Narrator" if msg.role == "system" else msg.role.capitalize()
            prompt += f"{role_label}: {msg.content}\n\n"
            
        prompt += "Narrator:"

        # 5. Stream and Collect
        full_content = ""
        async for token in llm_service.generate_stream(prompt, system_prompt=system_prompt):
            full_content += token
            yield token
            
        # 6. Persist response after stream is complete
        if full_content.strip():
            await self.add_message(db, branch_id, "assistant", full_content.strip())

    async def get_story_tree(self, db: AsyncSession, story_id: str):
        """
        Returns all branches and checkpoints for a given story.
        """
        branches = await branch_repository.get_multi_by_story(db, story_id)
        
        branch_ids = [b.id for b in branches]
        checkpoints = await checkpoint_repository.get_multi_by_branches(db, branch_ids)
        
        story = await story_repository.get(db, story_id)
        scenario_id = story.scenario_id if story else ""

        return {
            "story_id": story_id,
            "scenario_id": scenario_id,
            "branches": branches,
            "checkpoints": checkpoints
        }

    async def delete_last_message(self, db: AsyncSession, branch_id: str) -> bool:
        """
        Deletes the last message in a branch if it exists.
        """
        # Get last message for this branch
        query = select(Message).where(Message.branch_id == branch_id).order_by(Message.created_at.desc()).limit(1)
        result = await db.execute(query)
        last_msg = result.scalar_one_or_none()
        
        if last_msg:
            await db.delete(last_msg)
            await db.commit()
            return True
        return False

story_service = StoryService()
