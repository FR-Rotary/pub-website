from pycountry import countries

def to_pretty_name(numeric_code):
    return countries.get(numeric=str(numeric_code)).name

def to_letter_code(numeric_code):
    return countries.get(numeric=str(numeric_code)).alpha_3
