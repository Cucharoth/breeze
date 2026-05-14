import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_chronos_tree_logic(client: AsyncClient):
    # 1. Setup: Create a Scenario
    premise = "A space marine on Mars."
    scen_resp = await client.post("/api/v1/scenarios/", json={"premise": premise})
    scenario_id = scen_resp.json()["id"]
    
    # 2. Create a Story from the Scenario
    story_resp = await client.post(f"/api/v1/stories/?scenario_id={scenario_id}")
    assert story_resp.status_code == 201
    story = story_resp.json()
    story_id = story["id"]
    main_branch_id = story["main_branch_id"]
    
    # 3. Add messages to the Main Branch
    msg1_resp = await client.post(
        f"/api/v1/branches/{main_branch_id}/messages/", 
        json={"role": "user", "content": "Message 1"}
    )
    msg1_id = msg1_resp.json()["id"]
    
    msg2_resp = await client.post(
        f"/api/v1/branches/{main_branch_id}/messages/", 
        json={"role": "assistant", "content": "Message 2"}
    )
    msg2_id = msg2_resp.json()["id"]
    
    # 4. Create a Checkpoint at Message 2
    ckpt_resp = await client.post(
        f"/api/v1/branches/{main_branch_id}/checkpoints/",
        json={"message_id": msg2_id}
    )
    assert ckpt_resp.status_code == 201
    checkpoint_id = ckpt_resp.json()["id"]
    
    # 5. Spawn a new Branch from that Checkpoint
    branch_resp = await client.post(
        f"/api/v1/checkpoints/{checkpoint_id}/branches/",
        json={"name": "Alternate Timeline"}
    )
    assert branch_resp.status_code == 201
    alt_branch_id = branch_resp.json()["id"]
    
    # 6. Add a different message to the Alt Branch
    await client.post(
        f"/api/v1/branches/{alt_branch_id}/messages/", 
        json={"role": "user", "content": "Message 3 (Alt)"}
    )
    
    # 7. Verify Message Histories
    # Main Branch should have [Scenario, Msg 1, Msg 2]
    main_hist = await client.get(f"/api/v1/branches/{main_branch_id}/history/")
    main_contents = [m["content"] for m in main_hist.json()]
    assert "Message 1" in main_contents
    assert "Message 2" in main_contents
    assert "Message 3 (Alt)" not in main_contents
    
    # Alt Branch should have [Scenario, Msg 1, Msg 2, Msg 3 (Alt)]
    alt_hist = await client.get(f"/api/v1/branches/{alt_branch_id}/history/")
    alt_contents = [m["content"] for m in alt_hist.json()]
    assert "Message 1" in alt_contents
    assert "Message 2" in alt_contents
    assert "Message 3 (Alt)" in alt_contents
