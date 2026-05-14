import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_rolling_summary_logic(client, db_session):
    # 1. Setup: Create Scenario and Story
    scen_resp = await client.post("/api/v1/scenarios/", json={"premise": "A survival story."})
    scenario_id = scen_resp.json()["id"]
    story_resp = await client.post(f"/api/v1/stories/?scenario_id={scenario_id}")
    branch_id = story_resp.json()["main_branch_id"]

    # 2. Add many messages
    for i in range(10):
        await client.post(
            f"/api/v1/branches/{branch_id}/messages/", 
            json={"role": "user", "content": f"Message {i}"}
        )

    # 3. Mock LLM for summary
    mock_adapter = AsyncMock()
    mock_adapter.generate.return_value = "This is a summary of the first 5 messages."

    from app.api.dependencies import get_llm_adapter
    from app.main import app
    app.dependency_overrides[get_llm_adapter] = lambda: mock_adapter

    try:
        # 4. Trigger rolling summary (manual trigger for test, or automatic if implemented)
        # We'll implement an endpoint or a service call
        summ_resp = await client.post(f"/api/v1/branches/{branch_id}/summarize/")
        assert summ_resp.status_code == 200
        
        # 5. Verify summary exists
        data = summ_resp.json()
        assert "summary" in data
        assert "This is a summary" in data["summary"]
        
        # 6. Verify history still works (should include summary + remaining messages)
        hist_resp = await client.get(f"/api/v1/branches/{branch_id}/history/")
        # We need to decide how history returns summaries. 
        # Usually, the summary is the first "message" if older messages are pruned.
    finally:
        app.dependency_overrides.clear()
