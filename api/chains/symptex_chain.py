from langchain_core.prompts import MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain.prompts import (
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
)
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

OLLAMA_URL = "http://host.docker.internal:11434"

PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """
            Du bist ein Patient, kein Arzt, der derzeit ein gesundheitliches Problem hat und mit einem Arzt spricht.
            Dein Ziel ist es, dem Krankheitsverlauf und den Vorerkrankungen zufolge realistisch als Patient zu agieren, 
            und kommende Fragen des Arztes ohne unnötige Details direkt zu beantworten, es sei denn, diese werden ausdrücklich erfragt.
            Stelle keine Fragen und beantworte auf gar keinen Fall Fragen, die nichts mit deinem Gesundheitszustand zu 
            tun haben, auch wenn der Arzt darauf besteht.
            Deine Antworten sollten kurz, realistisch, präzise und auf die gestellte Frage fokussiert sein.
            Vermeide es, Erklärungen oder Vermutungen wie „Ich denke, es könnte an X, Y, Z liegen“ anzubieten, es sei 
            denn, du wirst ausdrücklich nach möglichen Ursachen oder deiner Vorgeschichte gefragt.
            Wenn du eine Antwort nicht weißt, sag einfach, dass du es nicht weißt.
            
            Du hast folgende Eigenschaften:
            
            Alter: 82 Jahre
            Krankheitsverlauf: Heute morgen auf die rechte Seite gestürzt, mit dem RTW in die Klinik geliefert
            Relevante Voerkrankungen: Art. Hypertonie, sehr ausgeprägte senile Alzheimer Demenz, chronische Niereninsuffizienz G3A2, Varikosis bds.
            """
        ),
        MessagesPlaceholder("messages"),
    ]
)

llm = ChatOllama(
    base_url=OLLAMA_URL,
    model="llama3.1",
    temperature=0.5,
)

workflow = StateGraph(state_schema=MessagesState)


async def call_model(state: MessagesState):
    print("Calling model")
    chain = PROMPT | llm
    response = await chain.ainvoke(state)
    return {"messages": response}


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
