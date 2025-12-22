import pandas as pd
import reverse_geocoder as rg
import pycountry

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

# Hàm phụ trợ để lấy tên đầy đủ từ mã quốc gia
def get_full_country_name(code):
    try:
        # pycountry.countries.get(alpha_2='VN') -> Country(alpha_2='VN', name='Viet Nam', ...)
        country = pycountry.countries.get(alpha_2=code)
        if country:
            return country.name
    except:
        pass
    return 'unknown' # Trả về unknown nếu không tìm thấy

