import pandas as pd

import config as cf

def fix_encoding(text):
    if pd.isna(text) or not isinstance(text, str):
        return text
    try:
        
        return text.encode('latin1').decode('utf-8')
    except:
        return text

def normalize_number(n):
    if not n:
        return None
    n = str(n).lower().strip().replace(",", "")

    # Xử lý "a few" thành "few"
    if n == "a few":
        n = "few"
    
    if n.isdigit():
        return int(n)

    if "-" in n:
        p = n.split("-")
        if len(p) == 2 and p[0] in cf.WORD_NUMBERS and p[1] in cf.WORD_NUMBERS:
            return cf.WORD_NUMBERS[p[0]] + cf.WORD_NUMBERS[p[1]]

    return cf.WORD_NUMBERS.get(n)

