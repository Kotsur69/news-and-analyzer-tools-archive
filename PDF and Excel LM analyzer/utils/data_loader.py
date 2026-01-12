# -*- coding: utf-8 -*-

import os
from utils.pdf_loader import load_pdf_text
from utils.excel_loader import load_excel_text
from tqdm import tqdm  # progress bar, opcjonalnie

def chunk_text(text, max_chars=4000):
    """Dzieli tekst na listę fragmentów o długości max_chars."""
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

def load_all_documents(chunk_size=4000):
    texts = []

    pdf_dir = "data/pdf"
    excel_dir = "data/excel"

    # 🔹 PDF-y
    if os.path.exists(pdf_dir):
        pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
        print(f"Znaleziono {len(pdf_files)} plików PDF w {pdf_dir}")

        for idx, file in enumerate(pdf_files, 1):
            print(f"[PDF {idx}/{len(pdf_files)}] Przetwarzanie pliku: {file}")
            text = load_pdf_text(os.path.join(pdf_dir, file))
            chunks = chunk_text(text, chunk_size)
            for c_idx, chunk in enumerate(chunks, 1):
                print(f"  Chunk {c_idx}/{len(chunks)} z pliku {file}")
                texts.append(chunk)

    # 🔹 Excel-e
    if os.path.exists(excel_dir):
        excel_files = [f for f in os.listdir(excel_dir) if f.lower().endswith(".xlsx")]
        print(f"Znaleziono {len(excel_files)} plików Excel w {excel_dir}")

        for idx, file in enumerate(excel_files, 1):
            print(f"[Excel {idx}/{len(excel_files)}] Przetwarzanie pliku: {file}")
            text = load_excel_text(os.path.join(excel_dir, file))
            chunks = chunk_text(text, chunk_size)
            for c_idx, chunk in enumerate(chunks, 1):
                print(f"  Chunk {c_idx}/{len(chunks)} z pliku {file}")
                texts.append(chunk)

    print(f"Łącznie chunków do analizy: {len(texts)}")
    return texts
