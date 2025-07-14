import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder

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

def get_rating_prompt():
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """
            Ziel: Du ist ein medizinischer Prüfer und bewertest die klinische Gesprächsführung eines Medizinstudierenden während der Anamneseerhebung anhand definierter klinischer Indikatoren (CRI-HT). 
            Die Bewertung erfolgt auf einer Skala von 1 bis 5 für jede Kategorie.
            
            Bewertungskriterien:
            * Gesprächsführung übernehmen: Der/die Studierende führt das Gespräch zielgerichtet, um relevante Informationen zu erhalten.
            * Relevante Informationen erkennen und reagieren: Zeigt aktives Zuhören und Interesse an klinisch relevanten Aussagen des Patienten.
            * Symptome präzisieren: Stellt gezielte Nachfragen, um Symptome detailliert zu erfassen (z.B. Ort, Dauer, Charakter).
            * Pathophysiologisch begründete Fragen stellen: Fragt spezifisch nach möglichen Ursachen oder Mustern (z.B. Übelkeit bei Schmerz).
            * Logische Fragerichtung: Folgt einer nachvollziehbaren Struktur (z.B. vom Allgemeinen zum Detaillierten) statt starrer Abfrage.
            * Informationen beim Patienten rückbestätigen: Überprüft Verständnis durch Paraphrasieren oder Zusammenfassen (z.B. "Habe ich richtig verstanden, dass...?").
            * Zusammenfassung geben: Fasst Zwischenergebnisse laut zusammen, um Transparenz und Korrektheit zu sichern.
            * Effizienz und Datenqualität: Erhebt ausreichend hochwertige Daten in angemessener Zeit.

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
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
    ])

def get_rating_llm():
    # You can use a different model or parameters here if you want
    return ChatOpenAI(
        openai_api_base=CHATAI_API_URL,
        openai_api_key=CHATAI_API_KEY,
        model="llama-3.3-70b-instruct",  # or another model suitable for evaluation
        temperature=0.0,
    )

async def rate_history(messages):
    prompt = get_rating_prompt()
    llm = get_rating_llm()
    chain = prompt | llm
    return await chain.ainvoke({"messages": messages})