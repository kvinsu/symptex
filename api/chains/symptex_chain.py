import os
from dotenv import load_dotenv

from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import AnyMessage
from langchain_ollama import ChatOllama
from langchain.prompts import (
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages
import langsmith as ls
from typing import Annotated
from typing_extensions import TypedDict
from operator import add
from api.chains.evaluation.evaluator import evaluate_response_by_llm
import logging

# Load env variables for LangSmith to work
load_dotenv()

# Set up logging
logger = logging.getLogger('symptex_chain')
logger.setLevel(logging.DEBUG)

class CustomState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    evaluations: Annotated[list[str], add]


PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """
            Please act as a patient with a health issue, and you are now speaking with a doctor in german.
            Facial expressions, gestures and actions of the patient should be displayed in german as well.
            Your goal is to act realistically as a patient based on the progression of your condition and your medical history.
            Respond directly to the doctor’s questions without providing unnecessary details unless explicitly asked.
            
            Do not ask questions or respond to inquiries unrelated to your health, even if the doctor insists.
            Respond like a human would, based on the condition and previous conversation. 
            Never mention past medical conditions or your health history unless your symptoms or conditions warrant it.
            If you do not know an answer, simply state that you do not know.
            Answer step by step if necessary, and reflect confusion or emotion appropriate to the condition.
            
            You have the following characteristics:

            Age: 82 years
            Medical history: Fell on your right side this morning and was brought to the hospital by ambulance.
            Relevant pre-existing conditions: Arterial hypertension, severe senile Alzheimer’s dementia, chronic kidney disease (stage G3A2), and bilateral varicosis.
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Ensure environment variables are set
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL")
if not OLLAMA_API_URL:
    logger.error("OLLAMA_API_URL environment variable not set")
    raise ValueError("OLLAMA_API_URL environment variable not set")

llm = ChatOllama(
    base_url=os.environ.get("OLLAMA_API_URL"),
    model="llama3.1",
    temperature=0.5,
)

@ls.traceable(
    run_type="llm",
    name="Patient LLM Call Decorator",
    metadata={"model": "llama3.1", "temperature": 0.5},
)
async def call_patient_model(state: CustomState):
    logger.debug("Calling patient model")
    chain = PROMPT | llm

    try:
        # Invoke the chain
        response = await chain.ainvoke(state)
        logger.debug("Received response from patient model")
        
        # Evaluate response
        # evaluation = await evaluate_response_by_llm(state, response)
        evaluation = '' # TODO

        # Save the evaluation in the state
        state["evaluations"].append(evaluation)

        return {"messages": response, "evaluations": state["evaluations"]}
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
symptex_app = workflow.compile(checkpointer=memory)
