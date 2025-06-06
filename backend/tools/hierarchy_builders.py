import pandas as pd
from dateutil.parser import parse

# Funzione centrale per pulizia valori
def clean_value(val):
    if pd.isnull(val):
        return None
    val = str(val).strip()
    if val == "":
        return None
    return val

def build_numeric_hierarchy(values, step=10, max_depth=3):
    hierarchy = {}
    for val in values:
        val = clean_value(val)
        if val is None:
            continue
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

def build_age_hierarchy(values):
    hierarchy = {}
    cleaned_values = []
    for v in values:
        v = clean_value(v)
        if v is None:
            continue
        try:
            fval = float(v)
            if 0 <= fval <= 120:
                cleaned_values.append(int(fval))
        except ValueError:
            continue

    values = sorted(set(cleaned_values))

    for age in values:
        current = str(age)

        # Livello 1 – blocchi di 5 anni
        b5_low = (age // 5) * 5
        b5_high = b5_low + 4
        l1 = f"{b5_low}-{b5_high}"
        hierarchy[current] = l1

        # Livello 2 – blocchi di 10 anni
        b10_low = (age // 10) * 10
        b10_high = b10_low + 9
        l2 = f"{b10_low}-{b10_high}"
        hierarchy[l1] = l2

        # Livello 3 – blocchi di 20 anni
        b20_low = (age // 20) * 20
        b20_high = b20_low + 19
        l3 = f"{b20_low}-{b20_high}"
        hierarchy[l2] = l3

         # Livello 4 – blocchi 0-39, 40-79, 80+
        if age <= 39:
            l4 = "0-39"
        elif age <= 79:
            l4 = "40-79"
        else:
            l4 = "80+"
        hierarchy[l3] = l4

        # Livello 5 – massimo livello
        hierarchy[l4] = "*"


    return hierarchy

def build_salary_hierarchy(values, steps=(10000, 20000), round_base=1000, max_depth=3):
    hierarchy = {}
    for val in values:
        val = clean_value(val)
        if val is None:
            continue
        try:
            salary = int(float(val))
        except (ValueError, TypeError):
            continue
        if salary < 0:
            continue
        level0 = str(round_base * round(salary / round_base))
        previous = level0
        for step in steps:
            low = (salary // step) * step
            high = low + step - 1
            label = f"{low//1000}k-{high//1000}k"
            hierarchy[previous] = label
            previous = label
        hierarchy[previous] = "*"
    return hierarchy

def build_zipcode_hierarchy(values):
    hierarchy = {}
    for code in values:
        code = clean_value(code)
        if code is None:
            continue
        if len(code) >= 5:
            hierarchy[code] = code[:4] + "*"
            hierarchy[code[:4] + "*"] = code[:3] + "**"
            hierarchy[code[:3] + "**"] = "*"
            #hierarchy[code[:3] + "**"] = code[:2] + "***" #eliminate perchè troppi livelli qui, facevano generalizzare troppo anche age, quindi meglio sacrificare solo zipcode e non entrambi (da scrivere nel report)
            #hierarchy[code[:2] + "***"] = "*"
        else:
            hierarchy[code] = "*" #equivalente di:
            #hierarchy[code[:3] + "**"] = "1" + "***" quando confronti coi test che hai creato
    return hierarchy

def build_categorical_hierarchy(values):
    return {clean_value(val): "*" for val in values if clean_value(val) is not None}

def build_email_domain_hierarchy(values):
    hierarchy = {}
    for val in values:
        val = clean_value(val)
        if val is None:
            continue
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
    hierarchy = {}
    for val in values:
        val = clean_value(val)
        if val is None:
            continue
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

# Builders generici
def generic_numeric_builder(values):
    return build_numeric_hierarchy(values, step=100, max_depth=2)

def generic_categorical_builder(values):
    return {clean_value(val): "*" for val in values if clean_value(val) is not None}

# Mapping QIs → builder
def get_builder_for_column(col_name, df):
    col_lower = col_name.lower()
    QI_HIERARCHY_BUILDERS = {
        "age": build_age_hierarchy,
        "year_of_birth": build_numeric_hierarchy,
        "calendar_year": build_numeric_hierarchy,
        "income": build_salary_hierarchy,
        "salary": build_salary_hierarchy,
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

    builder = QI_HIERARCHY_BUILDERS.get(col_lower)
    if builder:
        return builder
    if "year" in col_lower:
        return build_numeric_hierarchy
    if "date" in col_lower or "birth" in col_lower:
        return build_date_hierarchy
    if "zip" in col_lower or "postal" in col_lower:
        return build_zipcode_hierarchy
    if "email" in col_lower:
        return build_email_domain_hierarchy
    if pd.api.types.is_numeric_dtype(df[col_name]):
        return generic_numeric_builder
    else:
        return generic_categorical_builder
