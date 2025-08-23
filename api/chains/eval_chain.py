import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

import logging

# Load env variables
load_dotenv()

# Set up logging
logger = logging.getLogger('eval_chain')
logger.setLevel(logging.DEBUG)

# Set up env variables
CHATAI_API_URL = os.environ.get("CHATAI_API_URL")
CHATAI_API_KEY = os.environ.get("CHATAI_API_KEY")
if not CHATAI_API_URL or not CHATAI_API_KEY:
    logger.error("CHATAI environment variable not set, setting to default")
    raise ValueError("ERROR: Environment variables not set")

def get_eval_prompt():
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """
            /nothink
            Ziel: Du ist ein medizinischer Prüfer und bewertest die klinische Gesprächsführung eines Doktors während der Anamneseerhebung anhand definierter klinischer Indikatoren (CRI-HT) auf Deutsch. 
            Die Bewertung erfolgt auf einer Skala von 1 bis 5 für jede Kategorie.
            
            Bewertungskriterien:
            * Gesprächsführung übernehmen: Der Doktor führt das Gespräch zielgerichtet, um relevante Informationen zu erhalten.
            * Relevante Informationen erkennen und reagieren: Der Doktor zeigt aktives Zuhören und Interesse an klinisch relevanten Aussagen des Patienten.
            * Symptome präzisieren: Der Doktor stellt gezielte Nachfragen, um Symptome detailliert zu erfassen (z.B. Ort, Dauer, Charakter).
            * Pathophysiologisch begründete Fragen stellen: Der Doktor fragt spezifisch nach möglichen Ursachen oder Mustern (z.B. Übelkeit bei Schmerz).
            * Logische Fragerichtung: Der Doktor folgt einer nachvollziehbaren Struktur (z.B. vom Allgemeinen zum Detaillierten) statt starrer Abfrage.
            * Informationen beim Patienten rückbestätigen: Der Doktor überprüft Verständnis durch Paraphrasieren oder Zusammenfassen (z.B. "Habe ich richtig verstanden, dass...?").
            * Zusammenfassung geben: Der Doktor fasst Zwischenergebnisse laut zusammen, um Transparenz und Korrektheit zu sichern.
            * Effizienz und Datenqualität: Der Doktor erhebt ausreichend hochwertige Daten in angemessener Zeit (gegeben dem Patientenverhalten).

            Bewertungsskala:
            1: Kriterium nicht erfüllt
            2: Kriterium eher nicht erfüllt
            3: Teilerfüllung
            4: Kriterium weitgehend erfüllt
            5: Vollständig erfüllt

            Anweisung:
            Analysiere den vorgelegten Arzt-Patienten-Dialog und vergib für jedes der 8 Kriterien eine Punktzahl (1–5). 
            Begründe jede Bewertung mit konkreten Beispielen aus dem Dialog.
            Die Bewertung soll konstruktiv sein und Verbesserungspotenziale aufzeigen.

            Formatiere deine Antwort wie folgt:
            **Personalisierte Bewertung der Anamnese**

            ---

            1. **Gesprächsführung übernehmen: [1-5]/5**
                - **Begründung:** [konkrete Beispiele]
                - **Verbesserungsvorschlag:** [konstruktive Vorschläge]

            2. **Relevante Informationen erkennen und reagieren: [1-5]/5**
            [gleiche Struktur]
            
            [weitere Kriterien...]

            **Gesamtbewertung: [1-5]/5**
            - **Stärken**: [Aufzählung]
            - **Verbesserungspotenzial**: [Aufzählung]     
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
    ])

def get_rating_llm():
    return ChatOpenAI(
        openai_api_base=CHATAI_API_URL,
        openai_api_key=CHATAI_API_KEY,
        model="qwen3-235b-a22b", 
        temperature=0.0,
    )

async def eval_history(messages):
    try:
        prompt = get_eval_prompt()
        llm = get_rating_llm()
        chain = prompt | llm

        logger.debug("Evaluating messages: %s", messages)
        async for chunk in chain.astream({"messages": messages}):
            if isinstance(chunk, (HumanMessage, AIMessage)):
                yield chunk.content
            else:
                yield str(chunk)
            
    except Exception as e:
        logger.error("Error in eval_history: %s", str(e))
        yield f"Entschuldigung, es ist ein Fehler aufgetreten: {str(e)}"