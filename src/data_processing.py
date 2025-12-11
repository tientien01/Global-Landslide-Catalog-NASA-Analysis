import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#=============== TEXT ==================
def clean_text(text):
    if pd.isna(text): 
        return ""
    text = str(text).lower()
    # Xóa URL
    text = re.sub(r'http\S+', '', text)
    # Xóa ký tự không phải chữ cái hoặc số (giữ lại khoảng trắng)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Xóa khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()
    return text



# 1. Khởi tạo công cụ
lemmatizer = WordNetLemmatizer()
# Sử dụng Stopwords tiếng Anh (vì dữ liệu là GLC-NASA, chủ yếu dùng tiếng Anh)
english_stop_words = set(stopwords.words('english'))

def advanced_nlp_cleaning(text):
    # Bước 1: Tokenization (Tách từ)
    tokens = text.split() 
    
    cleaned_tokens = []
    for token in tokens:
        # Bước 2: Xóa Stop Words
        if token not in english_stop_words:
            # Bước 3: Lemmatization (Đưa về gốc)
            # Dùng 'v' (verb) làm mặc định cho độ chính xác cao hơn
            lemma = lemmatizer.lemmatize(token, pos='v') 
            
            cleaned_tokens.append(lemma)
            
    # Bước 4: Ghép lại thành chuỗi sạch
    return " ".join(cleaned_tokens)

