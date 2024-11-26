from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
import logging

from api.chains.symptex_chain import app

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()


# Input model
class ChatRequest(BaseModel):
    message: str

async def stream_response(message: str):
    # TODO thread_id for each session
    config = {"configurable": {"thread_id": "1"}}
    logger.debug("STREAMING")

    async for msg, metadata in app.astream(
        {"messages": [HumanMessage(message)]}, config, stream_mode="messages"):
        # Get AIMessageChunks only
        if msg.content and not isinstance(msg, HumanMessage):
            logger.debug(msg.content)
            yield msg.content

@router.post("/chat")
async def chat_with_llm(request: ChatRequest):
    try:
        logger.debug("Received request")
        return StreamingResponse(stream_response(request.message), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
