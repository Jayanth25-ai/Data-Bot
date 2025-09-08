import google.generativeai as genai
from google.api_core import exceptions
import logging

def generate_response(system_prompt, retrieved_chunks, user_query, api_key):
    try:
        genai.configure(api_key=api_key)
        # The 'gemini-pro' model alias can sometimes cause issues.
        # Using a more specific and recent model like 'gemini-1.5-flash-latest' is more reliable.
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        context = "\n\n".join(retrieved_chunks)
        prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion: {user_query}"
        response = model.generate_content(prompt)
        return response.text
    except exceptions.NotFound as e:
        logging.error(f"Model not found error: {e}")
        return "Error: The generative model was not found. Please check the model name and your API access."
    except Exception as e:
        logging.error(f"An unexpected error occurred while generating the response: {e}")
        return "Sorry, an error occurred while communicating with the AI service. Please check the application logs."