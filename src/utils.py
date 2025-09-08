import os

def get_api_key():
    return os.getenv("GOOGLE_API_KEY")  # Or use st.secrets["GOOGLE_API_KEY"]