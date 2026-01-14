# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime
import pandas as pd
from PyPDF2 import PdfReader

DATE_PATTERN = re.compile(r"(\d{4})\.(\d{2})")

# --------------------------------------------------
# Funkcje pomocnicze
# --------------------------------------------------
def extract_year_month(filename: str) -> str:
    match = DATE_PATTERN.search(filename)
    if not match:
        raise ValueError(f"Brak daty YYYY.MM w nazwie pliku: {filename}")
    return f"{match.group(1)}.{match.group(2)}"

def extract_datetime(filename: str) -> datetime:
    y, m = extract_year_month(filename).split(".")
    return datetime(int(y), int(m), 1)

def classify_role(filename: str) -> str:
    name = filename.lower()
    if "uzupelnienie" in name or "supplement" in name:
        return "supplement"
    if "context" in name or "macro" in name:
        return "context"
    return "core"

def chunk_text(text, max_chars=4000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

# --------------------------------------------------
# Ładowanie pojedynczego pliku PDF lub Excel
# --------------------------------------------------
def load_pdf_text(path):
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text
    except Exception as e:
        print(f"Błąd przy wczytywaniu PDF {path}: {e}")
        return ""

def load_excel_text(path):
    try:
        df = pd.read_excel(path)
        return df.to_string(index=False)
    except Exception as e:
        print(f"Błąd przy wczytywaniu Excel {path}: {e}")
        return ""

# --------------------------------------------------
# Funkcje publiczne dla main.py
# --------------------------------------------------

def _load_files(dir_path, file_ext, chunk_size=4000):
    """Wewnętrzna funkcja do wczytywania plików z katalogu."""
    if not os.path.exists(dir_path):
        return []

    files = [f for f in os.listdir(dir_path) if f.lower().endswith(file_ext)]
    files.sort(key=extract_datetime)

    result = []
    for f in files:
        role = classify_role(f)
        full_path = os.path.join(dir_path, f)
        text = load_pdf_text(full_path) if file_ext==".pdf" else load_excel_text(full_path)
        chunks = chunk_text(text, chunk_size)
        result.append({
            "filename": f,
            "type": "pdf" if file_ext==".pdf" else "excel",
            "role": role,
            "chunks": chunks
        })
        print(f"Załadowano: {f} | {role} | chunks: {len(chunks)}")
    return result

def load_pdfs(pdf_dir="data/pdf", chunk_size=4000):
    """Ładuje wszystkie PDF-y."""
    return _load_files(pdf_dir, ".pdf", chunk_size)

def load_excels(excel_dir="data/excel", chunk_size=4000):
    """Ładuje wszystkie Excel-e."""
    return _load_files(excel_dir, ".xlsx", chunk_size)

def merge_data(pdf_data, excel_data):
    """
    Scala dane PDF + Excel w timeline według YYYY.MM.
    Zwraca:
    {
        "2025.01": {"files": [...]},
        "2025.02": {"files": [...]},
        ...
    }
    """
    timeline = {}

    for file in pdf_data + excel_data:
        year_month = extract_year_month(file["filename"])
        if year_month not in timeline:
            timeline[year_month] = {"files": []}
        timeline[year_month]["files"].append(file)

    # Sortowanie miesięcy chronologicznie
    timeline = dict(sorted(timeline.items(), key=lambda x: extract_datetime(x[0])))
    print(f"📦 Dane scalone. Łącznie miesięcy: {len(timeline)}")
    return timeline
