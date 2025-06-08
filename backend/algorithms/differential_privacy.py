import pandas as pd
import numpy as np

def add_laplace_noise(series, epsilon, max_variation):
    """
    Aggiunge rumore laplaciano controllato: la variazione massima è circa ± max_variation.
    """
    scale = max_variation / epsilon
    noise = np.random.laplace(loc=0.0, scale=scale, size=len(series))
    noisy_series = series + noise
    # Clip per rientrare nella variazione consentita
    return np.clip(noisy_series, series - max_variation, series + max_variation)

def detect_age_column(columns):
    keywords = ["age", "patient_age", "birth_year"]
    for col in columns:
        if any(key in col.lower() for key in keywords):
            return col
    return None

def detect_zip_column(columns):
    keywords = ["zip", "zipcode", "postal", "postcode"]
    for col in columns:
        if any(key in col.lower() for key in keywords):
            return col
    return None

def truncate_zipcode(zip_series):
    return zip_series.astype(str).str[:3]

def randomized_response(series, epsilon, categories):
    """
    Implementazione semplificata di randomized response per colonna categorica.
    Restituisce una colonna perturbata.
    """
    p = np.exp(epsilon) / (np.exp(epsilon) + len(categories) - 1)
    
    def perturb_value(val):
        if val not in categories:
            return np.random.choice(categories)
        if np.random.rand() < p:
            return val
        else:
            other_cats = [c for c in categories if c != val]
            return np.random.choice(other_cats)
    
    return series.apply(perturb_value)

def apply_differential_privacy(df: pd.DataFrame, epsilon: float):
    """
    Applica Differential Privacy automaticamente alle colonne numeriche di un DataFrame.

    Args:
        df (pd.DataFrame): Dataset originale.
        epsilon (float): Privacy budget.

    Returns:
        pd.DataFrame: Dataset privatizzato.
    """
    df = df.copy()
    
    age_col = detect_age_column(df.columns)
    zip_col = detect_zip_column(df.columns)
    
    # Trattamento ZIP
    if zip_col and zip_col in df.columns:
        df[zip_col] = truncate_zipcode(df[zip_col])

     # Colonne numeriche da privatizzare (escludo ZIP)
    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and col != zip_col]

    
    # Clip valori numerici a intervalli ragionevoli per sensitività nota
    # Per età: 18-90 (già specificato)
    # Per altre colonne: utilizziamo 1° e 99° percentile per limitare outlier (più robusto)
    for col in numeric_cols:
        if col == age_col:
            max_variation = 5  # Età può cambiare di massimo ±5 anni
            df[col] = add_laplace_noise(df[col], epsilon, max_variation)
            df[col] = df[col].round().clip(18, 90).astype(int)
        else:
            max_variation = 1 / epsilon
            lower = df[col].quantile(0.01)
            upper = df[col].quantile(0.99)
            df[col] = df[col].clip(lower, upper)
            df[col] = add_laplace_noise(df[col], epsilon, max_variation).round()
                
    # Protezione di tutte le categoriche potenzialmente sensibili
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    # Colonne da escludere dalla perturbazione
    excluded = []  
    if zip_col:
        excluded.append(zip_col)

    # Rimuove le escluse dalla lista
    categorical_cols = [col for col in categorical_cols if col not in excluded]
    for col in categorical_cols:
        categories = df[col].dropna().unique().tolist()
        if len(categories) > 1:
            epsilon_cat = epsilon * 0.1  # uso frazione del budget per ogni categorica
            df[col] = randomized_response(df[col], epsilon_cat, categories)
    
    return df