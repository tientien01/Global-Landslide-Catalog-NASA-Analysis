import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag




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
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
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

# -------------------------------------------------------
WORD_NUMBERS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,

    "several": 3,
    "multiple": 3,
    "few": 3,
    "a few": 3,
    "some": 3,
    "many": 10,
    "dozens": 24,
    "dozen": 12,
    "scores": 40,
    "hundreds": 200,
    "thousands": 1000,
}

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
        if len(p) == 2 and p[0] in WORD_NUMBERS and p[1] in WORD_NUMBERS:
            return WORD_NUMBERS[p[0]] + WORD_NUMBERS[p[1]]

    return WORD_NUMBERS.get(n)

# ============================================================
#                       REGEX FIXED
# ============================================================

# Two separate numeric patterns with DIFFERENT group names
NUM_FATAL = r"(?P<fnum>\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|dozens?|scores|hundreds|thousands|several|multiple|many|few|some)"
NUM_INJ = r"(?P<inum>\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|dozens?|scores|hundreds|thousands|several|multiple|many|few|some)"

fatal_kw = r"(?:killed|dead|died|fatality|fatalities|death|deaths)"
inj_kw   = r"(?:injured|hurt|wounded|hospitalized|injuries)"

# Combined: X killed and Y injured (FIXED group names)
COMBINED = re.compile(
    rf"{NUM_FATAL}\s*(?:people|persons|individuals)?\s*{fatal_kw}\s*(?:,|and|with)?\s*"
    rf"{NUM_INJ}\s*(?:people|persons|individuals)?\s*{inj_kw}",
    re.IGNORECASE
)

# Single fatality pattern
FATAL = re.compile(
    rf"(?:at least|around|about|approximately|some|as many as|up to|over|more than)?\s*"
    rf"{NUM_FATAL}\s*(?:people|persons|individuals)?\s*(?:were|was|are|have been)?\s*{fatal_kw}",
    re.IGNORECASE
)

# Single injury pattern
INJ = re.compile(
    rf"(?:at least|around|about|approximately|some|as many as|up to|over|more than)?\s*"
    rf"{NUM_INJ}\s*(?:people|persons|individuals)?\s*(?:were|was|are|have been)?\s*{inj_kw}",
    re.IGNORECASE
)

# "no casualties" patterns
NO_CAS = re.compile(
    r"\b(?:no\s+(?:casualties|fatalities|injuries|deaths?)|"
    r"zero\s+(?:casualties|fatalities|injuries|deaths?)|"
    r"without\s+(?:any\s+)?(?:casualties|fatalities|injuries|deaths?))\b",
    re.IGNORECASE
)

# "no one was" patterns
NO_ONE = re.compile(
    r"\bno\s+(?:one|person|people)\s+(?:was|were)\s+(?:killed|dead|injured|hurt|wounded)\b",
    re.IGNORECASE
)

# ============================================================
#                    MAIN EXTRACTION FUNCTION
# ============================================================
def extract_casualties(text):
    """Extract fatalities and injuries from text. Returns (fatalities, injuries)"""
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return None, None

    text = str(text)
    
    # Check for "no casualties" first
    if NO_CAS.search(text):
        return 0, 0
    
    # Check for "no one was"
    no_one_match = NO_ONE.search(text)
    if no_one_match:
        text_part = no_one_match.group()
        if 'killed' in text_part or 'dead' in text_part:
            return 0, None
        elif 'injured' in text_part or 'hurt' in text_part or 'wounded' in text_part:
            return None, 0
    
    fatalities = None
    injuries = None
    
    # ---- COMBINED PATTERN ----
    m = COMBINED.search(text)
    if m:
        try:
            fatalities = normalize_number(m.group("fnum"))
            injuries = normalize_number(m.group("inum"))
            if fatalities is not None and injuries is not None:
                return fatalities, injuries
        except (IndexError, KeyError):
            pass  # Fall back to individual patterns
    
    # ---- INDIVIDUAL PATTERNS ----
    # Try fatalities
    if fatalities is None:
        m = FATAL.search(text)
        if m:
            fatalities = normalize_number(m.group("fnum"))
    
    # Try injuries
    if injuries is None:
        m = INJ.search(text)
        if m:
            injuries = normalize_number(m.group("inum"))
    
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
            fatalities = normalize_number(m.group(1))
    
    return fatalities, injuries


# ================================
# KIỂM TRA VỚI VÍ DỤ
# ================================
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
        print(f"  → Fatalities: {fatalities}, Injuries: {injuries}")
        print("-" * 60)




