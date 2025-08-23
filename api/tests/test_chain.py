import pytest
import httpx

API_URL = "http://localhost:8000/api/v1/chat"

@pytest.mark.asyncio
async def test_chat_default_condition():
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(API_URL, json={"message": "Wie geht es Ihnen?", "condition": "default"})
        assert response.status_code == 200
        text = ""
        async for chunk in response.aiter_text():
            text += chunk
        assert "Ich" in text or "mir" in text
        
@pytest.mark.asyncio
async def test_chat_default_patient():
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(API_URL, json={"message": "Haben Sie Vorerkrankungen?", "condition": "default"})
        assert response.status_code == 200
        text = ""
        async for chunk in response.aiter_text():
            text += chunk
        assert "keine" in text or "nein" in text

@pytest.mark.asyncio
async def test_chat_invalid_condition():
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(API_URL, json={"message": "Test", "condition": "invalid_condition"})
        assert response.status_code in (400, 422, 500)