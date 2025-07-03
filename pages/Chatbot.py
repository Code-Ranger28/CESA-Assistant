import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
import json # For logging chat history

# Configure Gemini API (using st.secrets for secure key management)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash") # Or your chosen model
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}. Please ensure your GEMINI_API_KEY is set in .streamlit/secrets.toml")
    st.stop() # Stop the app if API key is not configured

st.title("💬 AI Assistant Chat")
st.write("Start a conversation with your knowledgeable AI assistant.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a welcoming message from the assistant
    st.session_state.messages.append({"role": "assistant", "content": "Hello! How can I help you today?"})

# --- Helper for Logging Chat ---
LOG_FILE = "chat_logs.jsonl" # Using .jsonl for line-delimited JSON

def log_chat_interaction(user_query, bot_response):
    """Logs each interaction to a JSONL file."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_query": user_query,
        "bot_response": bot_response
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# --- Display chat messages from history on app rerun ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Accept user input ---
if prompt := st.chat_input("Ask me a question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Construct the full conversation history for the model
                conversation_for_model = [
                    {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
                    for msg in st.session_state.messages
                ]
                
                # Call Gemini API
                # Note: If you're using your original `generate()` function, you'd integrate it here.
                # For simplicity, I'm calling the model directly.
                response = model.generate_content(conversation_for_model)
                full_response = response.text
            except Exception as e:
                full_response = f"An error occurred: {e}"
                st.error(full_response)
                
            st.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Log the interaction
        log_chat_interaction(prompt, full_response)

# Optional: Clear chat history button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.experimental_rerun() # Rerun to clear the displayed messages