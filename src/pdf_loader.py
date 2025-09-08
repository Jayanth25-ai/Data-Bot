import PyPDF2
from src.text_chunker import clean_text, chunk_text  # Make sure this import works

def load_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return clean_text(text)

def load_and_chunk_pdf(pdf_path, chunk_size=100, overlap=50):
    raw_text = load_pdf_text(pdf_path)
    return chunk_text(raw_text, chunk_size, overlap)