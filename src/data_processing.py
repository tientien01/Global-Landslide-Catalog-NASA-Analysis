import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag

import sys
import os

import config as cf
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


# -------------- hàm tách từ để chuẩn bị bước vào giai đoạn model ------------------
# 1. Khởi tạo công cụ
lemmatizer = WordNetLemmatizer()
# Sử dụng Stopwords tiếng Anh (vì dữ liệu là GLC-NASA, chủ yếu dùng tiếng Anh)
english_stop_words = set(stopwords.words('english'))

def advanced_nlp_cleaning(text):
    # Tokenization
    tokens = word_tokenize(text)

    # POS tagging (xác định loại từ)
    tagged = pos_tag(tokens)

    cleaned_tokens = []

    for word, tag in tagged:
        if word not in english_stop_words:

            # Map POS tag → loại cho lemmatizer
            pos = 'n'   # default noun
            if tag.startswith('V'):
                pos = 'v'
            elif tag.startswith('J'):
                pos = 'a'
            elif tag.startswith('R'):
                pos = 'r'

            lemma = lemmatizer.lemmatize(word, pos=pos)
            cleaned_tokens.append(lemma)

    return " ".join(cleaned_tokens)

# -------- Từ event_description trích xuất ra cố fatalities và injuries ----------------
def extract_casualties(text):
    """Extract fatalities and injuries from text. Returns (fatalities, injuries)"""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return None, None

    text = str(text)
    
    # Check for "no casualties" first
    if cf.NO_CAS.search(text):
        return 0, 0
    
    # Check for "no one was"
    no_one_match = cf.NO_ONE.search(text)
    if no_one_match:
        text_part = no_one_match.group()
        if 'killed' in text_part or 'dead' in text_part:
            return 0, None
        elif 'injured' in text_part or 'hurt' in text_part or 'wounded' in text_part:
            return None, 0
    
    fatalities = None
    injuries = None
    
    # ---- COMBINED PATTERN ----
    m = cf.COMBINED.search(text)
    if m:
        try:
            fatalities = ut.normalize_number(m.group("fnum"))
            injuries = ut.normalize_number(m.group("inum"))
            if fatalities is not None and injuries is not None:
                return fatalities, injuries
        except (IndexError, KeyError):
            pass  # Fall back to individual patterns
    
    # ---- INDIVIDUAL PATTERNS ----
    # Try fatalities
    if fatalities is None:
        m = cf.FATAL.search(text)
        if m:
            fatalities = ut.normalize_number(m.group("fnum"))
    
    # Try injuries
    if injuries is None:
        m = cf.INJ.search(text)
        if m:
            injuries = ut.normalize_number(m.group("inum"))
    
    # Special case: "X people" without explicit keyword
    # Try to find patterns like "11 villagers buried"
    if fatalities is None:
        people_pattern = re.compile(
            r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)'
            r'\s+(?:people|persons|villagers|residents|workers|individuals)'
            r'\s+(?:buried|killed|dead|died|trapped)',
            re.IGNORECASE
        )
        m = people_pattern.search(text)
        if m:
            fatalities = ut.normalize_number(m.group(1))
    
    return fatalities, injuries



# KIỂM TRA VỚI VÍ DỤ
def test_extraction():
    test_cases = [
        "3 people were killed and 5 injured in the landslide",
        "at least 10 dead, with 15 injured",
        "no casualties were reported",
        "approximately twenty people died",
        "5 killed",
        "7 injuries reported",
        "the landslide resulted in 2 fatalities and 3 injuries",
        "dozens of people were killed",
        "a few people were hurt",
        "several fatalities and multiple injuries",
        "one person was killed",
        "two dead, three wounded",
        "over 100 people died in the disaster",
        "with no injuries",
        "casualties included 8 dead and 12 injured",
    ]
    
    for test in test_cases:
        fatalities, injuries = extract_casualties(test)
        print(f"Text: {test[:50]}...")
        print(f"Fatalities: {fatalities}, Injuries: {injuries}")
        print("-" * 60)

#=================================
#        Classification
#=================================

def categorize_fatality(fatality_count):
    if pd.isna(fatality_count):
        return 'unknown'
    
    if fatality_count == 0:
        return 'no_fatalities'          # Lớp 0: Không có thương vong
    elif 1 <= fatality_count <= 10:
        return 'minor_incident'         # Lớp 1: Sự cố nhỏ
    elif 11 <= fatality_count <= 100:
        return 'moderate_incident'      # Lớp 2: Sự cố trung bình
    elif 101 <= fatality_count <= 1000:
        return 'serious_disaster'       # Lớp 3: Thảm họa nghiêm trọng
    else:
        return 'major_catastrophe'      # Lớp 4: Thảm họa thảm khốc (>50 người)



