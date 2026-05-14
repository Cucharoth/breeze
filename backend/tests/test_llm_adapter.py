import pytest
from app.services.llm.ollama_adapter import OllamaAdapter
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_ollama_adapter_generate():
    # Setup adapter
    adapter = OllamaAdapter(base_url="http://localhost:11434", model="llama3")
    
    # Mock the internal call (e.g., using httpx)
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        from unittest.mock import MagicMock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "The generated lore."}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        response = await adapter.generate("Tell me about a cyberpunk world.")
        
        assert response == "The generated lore."
        mock_post.assert_called_once()
        # Verify it called the correct endpoint
        args, kwargs = mock_post.call_args
        assert "/api/generate" in args[0]
        assert kwargs["json"]["model"] == "llama3"
