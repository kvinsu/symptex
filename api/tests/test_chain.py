import pytest
from api.chains.symptex_chain import CustomState, symptex_model
from unittest.mock import AsyncMock, patch
from api.app.routers.chat import stream_response

@pytest.mark.asyncio
async def test_symptex_workflow():
    """Test the LangGraph workflow with valid state."""
    state = CustomState(messages=[], condition="default")
    result = symptex_model.run(state)
    
    assert result is not None
    assert "messages" in result
    assert len(result["messages"]) > 0
