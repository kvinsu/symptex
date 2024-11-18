import requests
import streamlit as st
import logging

API_URL = "http://host.docker.internal:8000/api/v1/chat"

logging.basicConfig(level=logging.DEBUG)

st.set_page_config(page_title="Symptex", page_icon="🤖")
st.title("Symptex")
st.info(
    "I'm not feeling well, what's going on with me?"
)

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

    data = {"message": prompt}

    with st.spinner("Thinking..."):
        response_placeholder = st.chat_message("assistant").markdown("")

        with requests.post(API_URL, json=data, stream=True) as response:
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