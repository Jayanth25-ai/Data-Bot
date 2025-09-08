import google.generativeai as genai

def get_embeddings(text, api_key):
    genai.configure(api_key=api_key)
    response = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    return response["embedding"]