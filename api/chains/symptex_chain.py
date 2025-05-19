import os
from dotenv import load_dotenv

from langchain_core.messages import AnyMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages
import langsmith as ls
from typing import Annotated
from typing_extensions import TypedDict
from operator import add
import logging

from api.chains.prompts import PROMPTS

# Load env variables for LangSmith to work
load_dotenv()

# Set up logging
logger = logging.getLogger('symptex_chain')
logger.setLevel(logging.DEBUG)

class CustomState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    condition: str
        
# Ensure environment variables are set
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL")
if not OLLAMA_API_URL:
    logger.error("OLLAMA_API_URL environment variable not set, setting to default")
    OLLAMA_API_URL = "http://ollama:11434"

llm = ChatOllama(
    base_url=OLLAMA_API_URL,
    # Change model and temperature here
    model="phi4-mini",
    temperature=0.5,
)

@ls.traceable(
    run_type="llm",
    name="Patient LLM Call Decorator",
    metadata={"model": "phi4-mini", "temperature": 0.5},
)
async def call_patient_model(state: CustomState):
    prompt_id = state.get("condition")
    logger.debug("Calling patient model with prompt_id: {prompt_id}")

    if prompt_id not in PROMPTS:
        logger.error("Prompt ID not found: %s", prompt_id)
        raise ValueError(f"Prompt ID {prompt_id} not found")
    
    # Get the prompt
    prompt = PROMPTS[prompt_id]
    chain = prompt | llm

    try:
        # Invoke the chain
        response = await chain.ainvoke(state)
        logger.debug("Received response from patient model")

        return {"messages": response}
    except Exception as e:
        logger.error("Error calling patient model: %s", str(e))
        raise

# Define new graph
workflow = StateGraph(state_schema=CustomState)

# Define patient llm node
workflow.add_node("patient_model", call_patient_model)

# Set entrypoint as 'patient_model'
workflow.add_edge(START, "patient_model")
workflow.add_edge("patient_model", END)

# Add memory
memory = MemorySaver()

# Compile into LangChain runnable
symptex_model = workflow.compile(checkpointer=memory)
