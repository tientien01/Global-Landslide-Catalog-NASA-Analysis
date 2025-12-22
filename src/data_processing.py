import pandas as pd
import re
import reverse_geocoder as rg

import utils as ut 



#=================================
#              TEXT
#=================================
def clean_text(text):
    """Basic clean text
    
    Keyword arguments:
    argument -- description
    Return: return_description

    Dùng để xoá các từ cơ bản, chuẩn hoá từ để phân tích eda
    """
    
    if pd.isna(text): 
        return ""
    text = str(text).lower()
    # Xóa URL
    text = re.sub(r'http\S+', '', text)
    # Xóa ký tự không phải chữ cái hoặc số (giữ lại khoảng trắng)
    text = re.sub(r'[^a-z0-9à-ỹ\s]', ' ', text)
    # Xóa khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()
    return text


#=================================
#        LOCATION FILLING
#=================================
def fill_missing_locations(row):
    # Chỉ xử lý nếu thiếu Country hoặc Admin Division VÀ có Tọa độ
    if (pd.isna(row['country_name']) or row['country_name'] == 'unknown' or 
        pd.isna(row['admin_division_name']) or row['admin_division_name'] == 'unknown'):
        
        # Kiểm tra tọa độ hợp lệ (Khác 0 và không NaN)
        if pd.notna(row['latitude']) and pd.notna(row['longitude']) and row['latitude'] != 0:
            try:
                coords = (row['latitude'], row['longitude'])
                results = rg.search(coords, mode=1) 
                if results:
                    location_info = results[0]
                    
                    
                    # Cập nhật Country nếu đang thiếu
                    if pd.isna(row['country_name']) or row['country_name'] == 'unknown':
                        cc_code = location_info['cc'] # Lấy mã 'VN'
                        # --- ĐOẠN MỚI: CHUYỂN MÃ THÀNH TÊN ---
    
                        row['country_name'] = ut.get_full_country_name(cc_code)
                    
                    # Cập nhật Admin Division (Tỉnh/Bang) nếu đang thiếu
                    if pd.isna(row['admin_division_name']) or row['admin_division_name'] == 'unknown':
                        if  location_info['admin1']:
                            row['admin_division_name'] = location_info['admin1']
                        else:
                            row['admin_division_name'] = 'unknown'
            except:
                pass
    return row



