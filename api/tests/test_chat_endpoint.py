from fastapi.testclient import TestClient
from api.app.main import app

client = TestClient(app)

def test_chat_endpoint_valid_request():
    """Test the /chat endpoint with a valid request."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello", "condition": "default"}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert len(response.text) > 0

"""

def test_chat_endpoint_invalid_condition():
    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello", "condition": "invalid_condition"}
    )
    assert response.status_code == 500
    """
