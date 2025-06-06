# config/keywords.py

IDENTIFIER_KEYWORDS = {
    "name", "id", "public_id", "ssn"
}

SENSITIVE_KEYWORDS = {
    "disease", "diagnosis", "condition", "health", "disability", "mental", "medication",
    "treatment", "therapy", "genetic", "sexual", "religion", "belief", "faith", "political",
    "ideology", "union", "criminal", "conviction", "race", "ethnic", "pregnancy", "fertility",
    "insurance", "social security", "tax", "citizenship", "immigration", "asylum", "salary", "income", "financial status",
    "medical_condition", "health_status", "mental_health", "physical_health", "surgery",
    "genetic_data", "genome", "hereditary_condition", "biometric_data", "fingerprint", "retina_scan",
    "face_recognition", "voice_pattern", "sexual_orientation", "sexual_preference", "sex_life",
    "religious_belief", "creed", "political_opinion", "political_affiliation", "party_membership",
    "philosophical_belief", "moral_belief", "criminal_record", "criminal_history", "offense",
    "ethnicity", "racial_origin", "skin_color", "tribal_affiliation", "HIV_status", "STD_status",
    "cancer_type", "chronic_disease", "pregnancy_status", "reproductive_health", "insurance_number",
    "social_security_number", "tax_id", "citizenship_status", "immigration_status", "asylum_status"
}

QUASI_IDENTIFIER_KEYWORDS = {
    "age", "birth", "zip", "post", "code", "city", "town", "municipality", "state", "province",
    "region", "gender", "sex", "race", "ethnic", "marital", "occupation", "job", "profession",
    "educ", "phone", "mobile", "email", "address", "street", "country", "nationality", "language",
    "year", "month", "birthdate", "year_of_birth", "date_of_birth", "zipcode", "postal_code",
    "postcode", "marital_status", "maritalstatus", "job_title", "education", "education_level",
    "degree", "phone_number", "telephone", "email_domain", "street_address", "household_size",
    "family_size", "num_children", "income", "salary", "financial_status"
}