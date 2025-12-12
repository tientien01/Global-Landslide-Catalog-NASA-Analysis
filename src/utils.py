import pandas as pd

def fix_encoding(text):
    if pd.isna(text) or not isinstance(text, str):
        return text
    try:
        
        return text.encode('latin1').decode('utf-8')
    except:
        return text
