import pandas as pd
import numpy as np

def add_laplace_noise(series, epsilon, max_variation):
    """
    Adds controlled Laplacian noise: the maximum variation is approximately ± max_variation.
    """
    # Ensure the series is numeric
    numeric_series = pd.to_numeric(series, errors='coerce')
    scale = max_variation / epsilon
    noise = np.random.laplace(loc=0.0, scale=scale, size=len(numeric_series))
    noisy_series = numeric_series + noise
    # Clip to stay within the allowed variation
    return np.clip(noisy_series, numeric_series - max_variation, numeric_series + max_variation)

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
    Simplified implementation of randomized response for a categorical column.
    Returns a perturbed column.
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
    Automatically applies Differential Privacy to the numeric columns of a DataFrame.

    Args:
        df (pd.DataFrame): Original dataset.
        epsilon (float): Privacy budget.

    Returns:
        pd.DataFrame: Privatized dataset.
    """
    df = df.copy()
    
    age_col = detect_age_column(df.columns)
    zip_col = detect_zip_column(df.columns)
    
    # ZIP code processing
    if zip_col and zip_col in df.columns:
        df[zip_col] = truncate_zipcode(df[zip_col])

    # Numeric columns to privatize (excluding ZIP)
    numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and col != zip_col]

    # Clip numeric values to reasonable intervals for known sensitivity
    # For age: 18-90 (already specified)
    # For other columns: use 1st and 99th percentile to limit outliers (more robust)
    for col in numeric_cols:
        if col == age_col:
            max_variation = 5  # Age can change by at most ±5 years
            df[col] = add_laplace_noise(df[col], epsilon, max_variation)
            df[col] = df[col].round().clip(18, 90).astype(int)
        else:
            max_variation = 1 / epsilon
            lower = df[col].quantile(0.01)
            upper = df[col].quantile(0.99)
            df[col] = df[col].clip(lower, upper)
            df[col] = add_laplace_noise(df[col], epsilon, max_variation).round()
                
    # Protect all potentially sensitive categorical columns
    categorical_cols = df.select_dtypes(include='object').columns.tolist()
    # Columns to exclude from perturbation
    excluded = []  
    if zip_col:
        excluded.append(zip_col)

    # Remove excluded columns from the list
    categorical_cols = [col for col in categorical_cols if col not in excluded]
    for col in categorical_cols:
        categories = df[col].dropna().unique().tolist()
        if len(categories) > 1:
            epsilon_cat = epsilon * 0.1  # use a fraction of the budget for each categorical
            df[col] = randomized_response(df[col], epsilon_cat, categories)
    
    return df