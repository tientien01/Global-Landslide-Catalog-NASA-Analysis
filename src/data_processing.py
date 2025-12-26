import pandas as pd
import reverse_geocoder as rg
from src import utils as ut



#=================================
#              TEXT
#=================================
def clean_text(text):
    """ Chuẩn hoá text về chữ thường và nếu là ô trống thì điền là unknown
    
    """
    
    # Nếu là giá trị rỗng (NaN) thì trả về 'unknown'
    if pd.isna(text):
        return "unknown"
    
    # Chuyển về chữ thường và xoá khoảng trắng thừa ở 2 đầu
    return str(text).lower().strip()


#=================================
#        LOCATION FILLING
#=================================
def fill_missing_locations(row):
    """Điền tên quốc gia và đơn vị hành chính (cấp 1) theo longtitude và latitude
    
    """
    
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

#=================================
#  CLIMATE ZONE CLASSIFICATION
#=================================
def get_5_climate_zones(lat):
    """Phân loại thành 5 vùng khí hậu: Tropical, Subtropical, Temperate, Subpolar, Polar
    
    """
    
    # Trả về unknown nếu không có toạ độ
    if pd.isna(lat): 
        return 'unknown'
    
    # Lấy trị tuyệt đối để tính chung cho cả Bắc và Nam bán cầu
    abs_lat = abs(lat)
    
    if abs_lat <= 23.5:
        return 'tropical'      # 0 - 23.5
    elif abs_lat <= 35:
        return 'subtropical'   # 23.5 - 35
    elif abs_lat <= 60:
        return 'temperate'     # 35 - 60
    elif abs_lat <= 66.5:
        return 'subpolar'      # 60 - 66.5
    else:
        return 'polar'         # > 66.5

def get_geo_region(row):
    """Phân loại vùng địa lý: North America, South America, Europe, Africa, South Asia, East Asia, SE Asia Oceania

    """
    
    lat = row['latitude']
    lon = row['longitude']
    
    # Nếu thiếu toạ độ thì trả về unknown
    if pd.isna(lat) or pd.isna(lon):
        return 'unknown'

    # Châu Mỹ
    if lon < -30:
        if lat > 8:
            return 'north_america'  # Bao gồm Canada, Mỹ, Mexico, Trung Mỹ và Caribbean
        else:
            return 'south_america'   # Từ Colombia trở xuống
            
    # Châu Âu và Phi
    elif lon < 60:
        if lat > 30: return 'europe'
        else: return 'africa'
            
    # Châu Á và úc 
    else:
        if lon < 95: return 'south_asia'
        else:
            if lat > 25: return 'east_asia'
            else: return 'se_asia_oceania' # ĐNA và Úc 