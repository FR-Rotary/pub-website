from pycountry import countries

def to_pretty_name(numeric_code):
    return countries.get(numeric=str(numeric_code)).name

def to_letter_code(numeric_code):
    country = countries.get(numeric=str(numeric_code))
    if country is None:
        print(f"Country not found for code: {numeric_code}")
        return "Unknown"
    return country.alpha_3
