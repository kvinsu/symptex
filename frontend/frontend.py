import requests
import streamlit as st
import logging
import uuid

API_URL = "http://host.docker.internal:8000/api/v1"

logging.basicConfig(level=logging.DEBUG)

st.set_page_config(page_title="Symptex", page_icon="🤖")
st.title("Symptex")
st.info(
    "Sprechen Sie hier mit dem zu behandelnden Patienten."
)

# Initialize session state for model, condition, and talkativeness
if "condition" not in st.session_state:
    st.session_state.model = "gemma-3-27b-it"
    st.session_state.condition = "alzheimer"
    st.session_state.talkativeness = "kurz angebunden"
    st.session_state.thread_id = str(uuid.uuid4())


# Define sidebar options
st.sidebar.selectbox(
    "Modell",
    options=["gemma-3-27b-it", "llama-3.3-70b-instruct", "llama-3.1-sauerkrautlm-70b-instruct", "qwq-32b", "mistral-large-instruct", "qwen3-235b-a22b"],
    key="model"
)
st.sidebar.selectbox(
    "Patientenrolle",
    options=["default", "alzheimer", "schwerhörig", "verdrängung"],
    key="condition"
)
st.sidebar.selectbox(
    "Gesprächsverhalten",
    options=["kurz angebunden", "ausgewogen", "ausschweifend"],
    key="talkativeness"
)

# Add a reset button to the sidebar
if st.sidebar.button("Chat zurücksetzen", use_container_width=True):
    try:
        # Clear backend memory for this thread
        response = requests.post(f"{API_URL}/reset/{st.session_state.thread_id}")
        if response.status_code == 200:
            # Generate new thread ID
            st.session_state.thread_id = str(uuid.uuid4())
            # Clear frontend messages
            st.session_state.messages = []
            st.rerun()
        else:
            st.error("Error resetting chat memory")
    except Exception as e:
        st.error(f"Could not reset chat memory: {str(e)}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

# Accept user input
if prompt := st.chat_input("Enter your question"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {
        "message": prompt,
        "model": st.session_state.model,
        "condition": st.session_state.condition,
        "talkativeness": st.session_state.talkativeness,
        "thread_id": st.session_state.thread_id
    }

    with st.spinner("Thinking..."):
        response_placeholder = st.chat_message("assistant").markdown("")

        with requests.post(API_URL + "/chat", json=data, stream=True) as response:
            if response.status_code == 200:
                streamed_text = ""
                for chunk in response.iter_content(chunk_size=None):
                    # Decode chunk and update the full response
                    streamed_text += chunk.decode()

                    # Update the placeholder with the incremented response
                    response_placeholder.markdown(streamed_text)
            else:
                output_text = """An error occurred while processing your message.
                Please try again or rephrase your message."""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": streamed_text,
        }
    )