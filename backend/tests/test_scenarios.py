import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_scenario(client: AsyncClient):
    # Test: Submit a Premise
    premise = "A cyberpunk detective in Neo-Tokyo investigating a ghost in the machine."
    response = await client.post(
        "/api/v1/scenarios/",
        json={"premise": premise}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["premise"] == premise
    assert "id" in data
    assert "world_lore" in data
    assert "first_scene" in data
    assert "character_profiles" in data
    assert len(data["character_profiles"]) > 0
