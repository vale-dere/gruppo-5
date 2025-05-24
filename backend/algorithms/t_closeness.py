import pandas as pd

def apply_t_closeness(df: pd.DataFrame, quasi_identifiers: list, sensitive_attr: str, t: float) -> pd.DataFrame:
    return df.copy()