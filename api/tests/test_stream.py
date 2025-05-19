import pytest
from unittest.mock import AsyncMock, patch
from api.app.routers.chat import stream_response

@pytest.mark.asyncio
async def test_stream_response():
    """Test the stream_response function with a valid message and condition."""
    mock_symptex_model = AsyncMock()
    import pytest
from unittest.mock import AsyncMock, patch
from api.app.routers.chat import stream_response

@pytest.mark.asyncio
async def test_stream_response():
    """Test the stream_response function with a valid message and condition."""
    mock_symptex_model = AsyncMock()
    mock_symptex_model.astream.return_value = AsyncMock()
    mock_symptex_model.astream.return_value.__aiter__.return_value = [
        {"content": "Mock response", "metadata": {}}
    ]

    with patch("api.app.routers.chat.symptex_model", mock_symptex_model):
        generator = stream_response("Hello", "default")
        responses = [msg async for msg in generator]

    assert len(responses) > 0
    assert "Mock response" in responses

@pytest.mark.asyncio
async def test_stream_response_invalid_condition():
    """Test the stream_response function with an invalid condition."""
    with pytest.raises(ValueError):
        generator = stream_response("Hello", "invalid_condition")
        async for _ in generator:
            pass