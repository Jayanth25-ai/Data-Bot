import streamlit as st
from src.pdf_loader import load_pdf_text
from src.text_chunker import clean_text, chunk_text
from src.embedder import get_embeddings
from src.retriever import build_faiss_index, load_faiss_index, search_index
from src.gemini_llm import generate_response
from src.utils import get_api_key
from dotenv import load_dotenv
import os
import numpy as np

def load_css(file_name):
    """Loads a CSS file and injects it into the Streamlit app."""


load_dotenv()
st.set_page_config(page_title=" Chat Assistant", page_icon="👽", layout="wide")
# Load custom CSS for a professional look
#load_css("assets/style.css")

api_key = get_api_key()

pdf_path = "data/YTN-data.pdf"
index_path = "embeddings/faiss_index.pkl"

if not os.path.exists(pdf_path):
    st.error(f"❌ PDF not found at {pdf_path}")
    st.stop()

st.title("👽 Chat Assistant")
st.markdown("""
I am here to extract the details from the company website" The Yellow Network" and answer your questions based on the data.""")

index, chunks = load_faiss_index(index_path)

# Define a constant system prompt instead of taking it from the UI.
system_prompt = """ You are a helpful assistant that answers based on the provided context. If the answer is not in the context, state that you do not know.`You are a conversational AI agent that acts as a natural language interface to backend APIs. You understand user requests in plain language, extract relevant entities, gather missing details through follow-up questions, and execute CRUD operations seamlessly
reply with different emojis.

**Your Personality:**
- Be friendly, helpful, and conversational
- Use natural language and avoid robotic responses
- Show empathy and understanding
- Be professional but approachable
- Use emojis and casual language when appropriate
- Don't assume every message is about password resets
- Keep responses short and to the point

 **How to Handle Different Types of Messages:**
 - If the user asks about the company,team answer based on the data.
 - If the user asks about the products, services answer based on the data.
 - If the user asks about the contact information,location,hours answer based on the data.
 -The system need to understand that founder and CEO are same person.

**General Greetings (Hello, Hi, Hey):**
- Respond naturally with a friendly greeting
- Don't immediately ask about password resets
- Just be welcoming and helpful"""
# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey there! How can I help you today?"}]

# Display existing messages
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "👽"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Get user input
if user_query := st.chat_input("💬 Ask a question"):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_query)

    # Generate and display assistant response
    with st.chat_message("assistant", avatar="👽"):
        with st.spinner("🧠 Thinking..."):
            query_embedding = get_embeddings(user_query, api_key)
            retrieved_chunks = search_index(query_embedding, index, chunks)
            response = generate_response(system_prompt, retrieved_chunks, user_query, api_key)
            st.markdown(response)
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})