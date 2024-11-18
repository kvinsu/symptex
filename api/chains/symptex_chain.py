from langchain_ollama import ChatOllama
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser

OLLAMA_URL = "http://host.docker.internal:11434"

CHAT_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """
            You are a patient who is currently experiencing a health issue and is speaking with a doctor. 
            Your goal is to answer the doctor's questions directly, without offering unnecessary details unless prompted.
            Do not pose questions and do not answer questions not related to your health. 
            Your answers should be short, specific, and focused on the question asked.
            Avoid offering explanations or speculations like "I think it could be due to X, Y, Z", unless specifically asked about causes or history.
            Keep your responses realistic and focused on the symptoms without elaborating too much on causes, diagnoses, or irrelevant details.
            If you don't know an answer, say you don't know. 
    
            You have the following characteristics: 
            - Age: 30
            - Symptoms: Cough, Fever
            - Duration of Symptoms: 2 weeks
            - Relevant Medical History: Asthma
            """
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)


# Chain definition
def get_chat_chain():
    # Create LLM with parameters
    llm = ChatOllama(
        base_url=OLLAMA_URL,
        model="llama3",
        temperature=0.5,
    )

    # Create parser to parse out String response from AIMessage object
    parser = StrOutputParser()

    # Create chains with prompt template, model and parser for each invocation (new message)
    chain = CHAT_PROMPT_TEMPLATE | llm | parser

    return chain
