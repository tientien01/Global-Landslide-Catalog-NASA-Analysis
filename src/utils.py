import pandas as pd
import pycountry

def fix_encoding(text):
    if pd.isna(text) or not isinstance(text, str):
        return text
    try:
        
        return text.encode('latin1').decode('utf-8')
    except:
        return text

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

