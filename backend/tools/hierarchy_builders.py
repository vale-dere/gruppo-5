import pandas as pd

def build_numeric_hierarchy(values, step=10, max_depth=3):
    """
    Generalizes numeric values by grouping into ranges.
    """
    hierarchy = {}
    for val in values:
        try:
            num = int(float(val))
        except ValueError:
            continue
        current = str(num)
        for d in range(max_depth):
            step_size = step * (10 ** d)
            low = (num // step_size) * step_size
            high = low + step_size - 1
            general = f"{low}-{high}"
            hierarchy[current] = general
            current = general
        hierarchy[current] = "*"
    return hierarchy

def build_zipcode_hierarchy(values):
    hierarchy = {}
    for code in values:
        code = str(code)
        if len(code) >= 5:
            hierarchy[code] = code[:4] + "*"
            hierarchy[code[:4] + "*"] = code[:3] + "**"
            hierarchy[code[:3] + "**"] = code[:2] + "***"
            hierarchy[code[:2] + "***"] = "*"
        else:
            hierarchy[code] = "*"
    return hierarchy

def build_categorical_hierarchy(values):
    """
    Maps categories to '*'
    """
    return {val: "*" for val in values}

def build_email_domain_hierarchy(values):
    hierarchy = {}
    for val in values:
        if "@" in val:
            domain = val.split("@")[-1]
        else:
            domain = val
        parts = domain.split(".")
        if len(parts) > 2:
            general = ".".join(parts[-2:])
        else:
            general = domain
        hierarchy[val] = general
        hierarchy[general] = "*"
    return hierarchy

def build_date_hierarchy(values):
    """
    Generalizes dates progressively to year/month/decade/century
    """
    from dateutil.parser import parse
    import datetime

    hierarchy = {}
    for val in values:
        try:
            date = parse(str(val), fuzzy=True)
        except Exception:
            continue
        current = date.strftime("%Y-%m-%d")
        month = date.strftime("%Y-%m")
        year = date.strftime("%Y")
        decade = f"{year[:3]}0s"
        century = f"{year[:2]}00s"

        hierarchy[current] = month
        hierarchy[month] = year
        hierarchy[year] = decade
        hierarchy[decade] = century
        hierarchy[century] = "*"
    return hierarchy

# Mapping QIs to builder functions
QI_HIERARCHY_BUILDERS = {
    "age": build_numeric_hierarchy,
    "year_of_birth": build_numeric_hierarchy,
    "income": build_numeric_hierarchy,
    "salary": build_numeric_hierarchy,

    "zipcode": build_zipcode_hierarchy,
    "postal_code": build_zipcode_hierarchy,
    "zip": build_zipcode_hierarchy,
    "postcode": build_zipcode_hierarchy,

    "city": build_categorical_hierarchy,
    "town": build_categorical_hierarchy,
    "municipality": build_categorical_hierarchy,

    "state": build_categorical_hierarchy,
    "province": build_categorical_hierarchy,
    "region": build_categorical_hierarchy,
    "country": build_categorical_hierarchy,
    "nationality": build_categorical_hierarchy,
    "language": build_categorical_hierarchy,

    "education": build_categorical_hierarchy,
    "education_level": build_categorical_hierarchy,
    "degree": build_categorical_hierarchy,

    "occupation": build_categorical_hierarchy,
    "job_title": build_categorical_hierarchy,
    "profession": build_categorical_hierarchy,

    "race": build_categorical_hierarchy,
    "ethnicity": build_categorical_hierarchy,
    "gender": build_categorical_hierarchy,
    "sex": build_categorical_hierarchy,
    "marital_status": build_categorical_hierarchy,
    "maritalstatus": build_categorical_hierarchy,

    "email": build_email_domain_hierarchy,
    "email_domain": build_email_domain_hierarchy,

    "birthdate": build_date_hierarchy,
    "date_of_birth": build_date_hierarchy,

    "address": build_categorical_hierarchy,
    "street": build_categorical_hierarchy,
    "street_address": build_categorical_hierarchy,

    "phone_number": build_categorical_hierarchy,
    "telephone": build_categorical_hierarchy,

    "financial_status": build_categorical_hierarchy,
    "household_size": build_numeric_hierarchy,
    "family_size": build_numeric_hierarchy,
    "num_children": build_numeric_hierarchy,
}