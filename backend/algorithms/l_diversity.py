import pandas as pd

def apply_l_diversity(df: pd.DataFrame, quasi_identifiers: list, sensitive_attr: str, l: int) -> pd.DataFrame:
    return df.copy()