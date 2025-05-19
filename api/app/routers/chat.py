from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
import logging
from typing import AsyncGenerator

from api.chains.symptex_chain import symptex_model

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()


# Custom input model
class ChatRequest(BaseModel):
    message: str
    condition: str = "default"

async def stream_response(message: str, condition: str) -> AsyncGenerator[str, None]:
    """
    Stream responses from the symptex_app.

    Args:
        message (str): The input message from the user.
        condition (str): The medical condition to simulate.

    Yields:
        str: The response message from the LLM.
    """
    # TODO thread_id for each session
    config = {"configurable": {"thread_id": "1"}}
    logger.debug("Starting to stream response for message: %s", message)

    try:
        async for msg, metadata in symptex_model.astream(
            {
                "messages": [HumanMessage(message)],
                "condition": condition,
            },
            config, 
            stream_mode="messages"
        ):
            # Get AIMessageChunks only
            if msg.content and not isinstance(msg, HumanMessage):
                # logger.debug(msg.content)
                yield msg.content
    except Exception as e:
        logger.error("Error while streaming response: %s", str(e))
        raise

@router.post("/chat")
async def chat_with_llm(request: ChatRequest) -> StreamingResponse:
    """
    Endpoint to chat with the LLM.

    Args:
        request (ChatRequest): The request containing the user's message.

    Returns:
        StreamingResponse: The streaming response from the LLM.
    """
    try:
        logger.debug(f"Received chat request with message: {request.message}, condition: {request.condition}")
        return StreamingResponse(
            stream_response(request.message, condition=request.condition), 
            media_type="text/plain"
        )
    except Exception as e:
        logger.error("Error in chat_with_llm endpoint: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
