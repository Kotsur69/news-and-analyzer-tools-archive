import pandas as pd

def load_excel_text(path):
    df = pd.read_excel(path)
    return df.to_string(index=False)
