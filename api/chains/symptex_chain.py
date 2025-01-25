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


class CustomState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    evaluations: Annotated[list[str], add]


PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """
            Please act as a patient with a health issue, and you are now speaking with a doctor in german.
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

# Load env variables for LangSmith to work
load_dotenv()

llm = ChatOllama(
    base_url=os.environ.get("OLLAMA_API_URL"),
    model="mixtral",
    temperature=0.5,
)

@ls.traceable(
    run_type="llm",
    name="Patient LLM Call Decorator",
    metadata={"model": "mixtral", "temperature": 0.5},
)
async def call_patient_model(state: CustomState):
    print("Calling patient model")
    chain = PROMPT | llm

    # Invoke the chain
    response = await chain.ainvoke(state)

    # Evaluate response
    # evaluation = await evaluate_response_by_llm(state, response)

    return {"messages": response}



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
