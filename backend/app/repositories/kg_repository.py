from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.kg_node import KGNode
from app.models.kg_edge import KGEdge
from typing import List

class KGRepository:
    async def get_nodes(self, db: AsyncSession, branch_id: int) -> List[KGNode]:
        result = await db.execute(select(KGNode).where(KGNode.branch_id == branch_id))
        return list(result.scalars().all())

    async def get_edges(self, db: AsyncSession, branch_id: int) -> List[KGEdge]:
        result = await db.execute(select(KGEdge).where(KGEdge.branch_id == branch_id))
        return list(result.scalars().all())

    async def add_node(self, db: AsyncSession, branch_id: int, name: str, node_type: str, description: str = None) -> KGNode:
        # Check if node already exists in this branch
        result = await db.execute(
            select(KGNode).where(KGNode.branch_id == branch_id, KGNode.name == name)
        )
        existing = result.scalars().first()
        if existing:
            return existing
            
        node = KGNode(branch_id=branch_id, name=name, type=node_type, description=description)
        db.add(node)
        await db.flush()
        await db.refresh(node)
        return node

    async def add_edge(self, db: AsyncSession, branch_id: int, source_id: int, target_id: int, rel: str) -> KGEdge:
        edge = KGEdge(branch_id=branch_id, source_node_id=source_id, target_node_id=target_id, relationship=rel)
        db.add(edge)
        await db.flush()
        await db.refresh(edge)
        return edge

kg_repository = KGRepository()
