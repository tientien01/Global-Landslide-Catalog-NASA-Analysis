import re

#=========== GLOBAL VARIABLES ===========
RAW_DATA =  r"..\data\raw\Global_Landslide_Catalog_Export.csv"
PROCESSED_DATA = r"..\data\processed\Global_Landslide_Processed.csv"

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


#=========== REGEX PATTERNS FOR CASUALTIES EXTRACTION ===========

# Combined: X killed and Y injured
fatal_kw = r"(?:killed|dead|died|fatality|fatalities|death|deaths)"
inj_kw   = r"(?:injured|hurt|wounded|hospitalized|injuries)"

NUM_FATAL = r"(?P<fnum>\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|dozens?|scores|hundreds|thousands|several|multiple|many|few|some)"
NUM_INJ = r"(?P<inum>\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|dozens?|scores|hundreds|thousands|several|multiple|many|few|some)"

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

