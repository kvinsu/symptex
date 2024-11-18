from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from api.chains.symptex_chain import get_chat_chain

router = APIRouter()


# Input model
class ChatRequest(BaseModel):
    message: str


# Dependency to get the chain
def chat_chain():
    return get_chat_chain()


@router.post("/chat")
async def chat_with_llm(request: ChatRequest, chain=Depends(chat_chain)):
    try:
        return StreamingResponse(chain.astream(request.message), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
