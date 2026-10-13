import customtkinter as ctk
from tkinter import messagebox
import json
from analyzer import LMAnalyzer  # singleton z analyzer.py

# --- Pliki --- #
HISTORY_FILE = "history.json"
URLS_FILE = "urls.txt"

# --- CustomTkinter settings --- #
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# --- Funkcje pomocnicze --- #
def load_history_urls():
    """Ładuje historyczne URL-e z pliku"""
    urls = []
    try:
        with open(URLS_FILE, "r", encoding="utf-8") as f:
            urls.extend([line.strip() for line in f if line.strip()])
    except FileNotFoundError:
        pass
    return urls

def save_urls(urls):
    """Zapisuje URL-e do pliku"""
    with open(URLS_FILE, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")

def add_new_url():
    url = new_url_entry.get().strip()
    if not url:
        return
    if url not in all_urls:
        all_urls.append(url)
        var = ctk.BooleanVar(value=True)
        checkbox = ctk.CTkCheckBox(new_url_frame, text=url, variable=var)
        checkbox.pack(anchor="w", padx=10, pady=2)
        new_url_vars.append((url, var))
        save_urls(all_urls)
    new_url_entry.delete(0, "end")

def start_analysis():
    selected_urls = []

    # historyczne URL-e
    for url, var in history_url_vars:
        if var.get():
            selected_urls.append(url)

    # nowe URL-e
    for url, var in new_url_vars:
        if var.get():
            selected_urls.append(url)

    if not selected_urls:
        messagebox.showinfo("Uwaga", "Nie zaznaczono żadnych URLi do analizy.")
        return

    try:
        analyzer = LMAnalyzer.get_instance()
        analysis = analyzer.analyze(selected_urls)

        # Pokazanie wyniku w polu tekstowym
        analysis_text.configure(state="normal")
        analysis_text.delete("1.0", "end")

        # Jeżeli analiza jest JSON-em, ładnie formatuj
        if isinstance(analysis, dict):
            analysis_text.insert("1.0", json.dumps(analysis, indent=2, ensure_ascii=False))
        else:
            analysis_text.insert("1.0", str(analysis))

        analysis_text.configure(state="disabled")

        messagebox.showinfo("Gotowe", "Analiza zakończona!")

    except Exception as e:
        messagebox.showerror("Błąd", str(e))

# --- GUI --- #
root = ctk.CTk()
root.title("Steel Market Analyzer")
root.geometry("1000x750")

# --- Historyczne URL-e --- #
history_frame = ctk.CTkFrame(root)
history_frame.pack(fill="x", padx=20, pady=10)
ctk.CTkLabel(history_frame, text="Historyczne URL-e:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=5)

all_urls = load_history_urls()
history_url_vars = []
for url in all_urls:
    var = ctk.BooleanVar(value=True)
    checkbox = ctk.CTkCheckBox(history_frame, text=url, variable=var)
    checkbox.pack(anchor="w", padx=10, pady=2)
    history_url_vars.append((url, var))

# --- Dodawanie nowych URL-i --- #
new_url_frame = ctk.CTkFrame(root)
new_url_frame.pack(fill="x", padx=20, pady=10)
ctk.CTkLabel(new_url_frame, text="Dodaj nowe URL-e:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=5)

new_url_entry = ctk.CTkEntry(new_url_frame)
new_url_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
add_button = ctk.CTkButton(new_url_frame, text="Dodaj", command=add_new_url)
add_button.pack(side="right", padx=5)

new_url_vars = []

# --- Przycisk uruchamiający analizę --- #
start_button = ctk.CTkButton(root, text="Uruchom analizę", command=start_analysis, fg_color="#1E90FF")
start_button.pack(pady=10)

# --- Pole tekstowe z analizą --- #
analysis_frame = ctk.CTkFrame(root)
analysis_frame.pack(fill="both", expand=True, padx=20, pady=10)

ctk.CTkLabel(analysis_frame, text="Raport analizy rynku stali", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

analysis_text = ctk.CTkTextbox(analysis_frame, wrap="word")
analysis_text.pack(fill="both", expand=True)
analysis_text.insert("1.0", "Brak historii analiz.")
analysis_text.configure(state="disabled")

# --- Uruchom GUI --- #
root.mainloop()
