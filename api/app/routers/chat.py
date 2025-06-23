from fastapi import APIRouter
from fastapi.responses import StreamingResponse, PlainTextResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
import logging
from typing import AsyncGenerator
from api.chains.symptex_chain import memory

from starlette.responses import PlainTextResponse, StreamingResponse

from api.chains.symptex_chain import symptex_model

# Set up logging
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()


# Custom input model
class ChatRequest(BaseModel):
    message: str
    model: str
    condition: str
    talkativeness: str
    thread_id: str

@router.post("/chat")
async def chat_with_llm(request: ChatRequest):
    """
    Endpoint to chat with the LLM.
    """
    logger.debug("Received chat request: %s", request)
   
    # Validate message, condition and talkativeness BEFORE starting the stream
    if not request.message:
        logger.error("Empty message received")
        raise PlainTextResponse("Message cannot be empty", status_code=400)
    if request.model not in ["gemma-3-27b-it", "llama-3.3-70b-instruct", "llama-3.1-sauerkrautlm-70b-instruct", "qwq-32b", "mistral-large-instruct", "qwen3-235b-a22b"]:
        logger.error("Invalid model: %s", request.model)
        raise PlainTextResponse(f"Invalid model: {request.model}", status_code=400)
    if request.condition not in ["default", "alzheimer", "schwerhörig", "verdrängung"]:
        logger.error("Invalid condition: %s", request.condition)
        raise PlainTextResponse(f"Invalid condition: {request.condition}", status_code=400)
    if request.talkativeness not in ["kurz angebunden", "ausgewogen", "ausschweifend"]:
        logger.error("Invalid talkativeness: %s", request.talkativeness)
        raise PlainTextResponse(f"Invalid talkativeness: {request.talkativeness}", status_code=400)
        
    try:
        return StreamingResponse(
            stream_response(
                message=request.message, 
                model=request.model, 
                condition=request.condition, 
                talkativeness=request.talkativeness,
                thread_id=request.thread_id
            ), 
            media_type="text/plain"
        )
    except Exception as e:
        logger.error("Error in chat_with_llm endpoint: %s", str(e))
        return PlainTextResponse("Internal server error", status_code=500)
    
# Add reset endpoint
@router.post("/reset/{thread_id}")
async def reset_memory(thread_id: str):
    """Reset the LangChain memory for a specific thread"""
    try:
        # Delete thread from memory
        memory.delete_thread(thread_id)
        return PlainTextResponse(f"Chat memory cleared for thread {thread_id}", status_code=200)
    except Exception as e:
        logger.error(f"Error clearing memory for thread {thread_id}: {str(e)}")
        return PlainTextResponse("Error clearing chat memory", status_code=500)


async def stream_response(message: str, model: str, condition: str, talkativeness: str, thread_id: str) -> AsyncGenerator[str, None]:
    """
    Stream responses from the symptex_app.

    Args:
        message (str): The input message from the user.
        model (str): The model to use for generating the response.
        condition (str): The medical condition to simulate.
        talkativeness (str): The level of talkativeness for the response.
        history (List[Dict]): The chat history to maintain context.
        thread_id (str): The ID of the chat thread.

    Returns:
        str: The response message from the LLM.
    """
    config = {"configurable": {"thread_id": thread_id}}
    logger.debug("Starting to stream response for message: %s", message)

    try:
        async for msg, metadata in symptex_model.astream(
            {
                "messages": [HumanMessage(message)],
                "model": model,
                "condition": condition,
                "talkativeness": talkativeness,
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