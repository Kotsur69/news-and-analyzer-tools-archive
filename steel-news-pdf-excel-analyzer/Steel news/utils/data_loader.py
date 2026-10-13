import os
from utils.pdf_loader import load_pdf_text
from utils.excel_loader import load_excel_text

# Funkcja dzieląca tekst na fragmenty po max_chars
def chunk_text(text, max_chars=3000):
    """Dzieli tekst na listę fragmentów o długości max_chars."""
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

def load_all_documents(chunk_size=3000):
    texts = []

    pdf_dir = "data/pdf"
    excel_dir = "data/excel"

    # PDF-y
    if os.path.exists(pdf_dir):
        for file in os.listdir(pdf_dir):
            if file.lower().endswith(".pdf"):
                text = load_pdf_text(os.path.join(pdf_dir, file))
                chunks = chunk_text(text, chunk_size)
                texts.extend(chunks)

    # Excel-e
    if os.path.exists(excel_dir):
        for file in os.listdir(excel_dir):
            if file.lower().endswith(".xlsx"):
                text = load_excel_text(os.path.join(excel_dir, file))
                chunks = chunk_text(text, chunk_size)
                texts.extend(chunks)

    return texts  # <-- ZAWSZE lista, nawet jeśli pusta
