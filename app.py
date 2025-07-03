import streamlit as st

st.set_page_config(
    page_title="Sophisticated Chatbot & Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("Welcome to your AI Assistant Dashboard")
st.write("Navigate using the sidebar to the Chatbot or the Dashboard.")

# You can add some introductory text or images here.
# Streamlit's multi-page app feature automatically creates the sidebar navigation
# based on the files in the 'pages' directory.