import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.services.llm.base import LLMAdapter

@pytest.mark.asyncio
async def test_kg_extraction_background_task(client, db_session):
    # 1. Setup: Create Scenario and Story
    scen_resp = await client.post("/api/v1/scenarios/", json={"premise": "Space marine on Mars"})
    scenario_id = scen_resp.json()["id"]
    story_resp = await client.post(f"/api/v1/stories/?scenario_id={scenario_id}")
    branch_id = story_resp.json()["main_branch_id"]

    # 2. Mock LLM Adapter
    mock_adapter = AsyncMock(spec=LLMAdapter)
    mock_adapter.generate.return_value = '{"entities": [{"name": "Mars", "type": "Location", "description": "The red planet"}], "relationships": []}'

    from app.api.dependencies import get_llm_adapter
    from app.main import app
    
    app.dependency_overrides[get_llm_adapter] = lambda: mock_adapter

    try:
        # 3. Add a message to trigger extraction
        await client.post(
            f"/api/v1/branches/{branch_id}/messages/", 
            json={"role": "user", "content": "I land on the red sands of Mars."}
        )
        
        # Give background task a moment to finish
        # Since it's a separate task, we might need more than 0.1s or a retry loop
        for _ in range(10):
            await asyncio.sleep(0.2)
            kg_resp = await client.get(f"/api/v1/branches/{branch_id}/kg/")
            nodes = kg_resp.json()["nodes"]
            if len(nodes) > 0:
                break
    finally:
        app.dependency_overrides.clear()

        # 4. Verify KG content
        kg_resp = await client.get(f"/api/v1/branches/{branch_id}/kg/")
        assert kg_resp.status_code == 200
        nodes = kg_resp.json()["nodes"]
        assert len(nodes) > 0
        assert any(n["name"] == "Mars" for n in nodes)
