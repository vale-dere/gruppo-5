import pandas as pd

def generalize_column(column, level):
    """Generalize a column based on the level."""
    if pd.api.types.is_numeric_dtype(column):
        return column.apply(lambda x: f"{(x // 10**level) * 10**level}-{((x // 10**level) + 1) * 10**level - 1}") #ex. 20 -> 20-29
    else:
        return column.apply(lambda x: x[:max(0, len(x)-level)] + "*" * level) #ex. "12345" -> "123**"

def is_k_anonymous(df, quasi_identifiers, k):
    """Check if dataframe satisfies k-anonymity."""
    groups = df.groupby(quasi_identifiers).size()
    return (groups >= k).all()

def apply_k_anonymity(df: pd.DataFrame, quasi_identifiers: list, k: int, max_generalization: int = 3) -> pd.DataFrame:
    """Apply k-anonymity via generalization of quasi-identifiers."""
    # max_generalization is the maximum level of generalization allowed, 3 is a bilanced standard
    df = df.copy()
    for level in range(max_generalization + 1):
        temp_df = df.copy()
        for qi in quasi_identifiers:
            temp_df[qi] = generalize_column(temp_df[qi], level)
        if is_k_anonymous(temp_df, quasi_identifiers, k):
            print(f"[k-Anonymity] Raggiunto con generalizzazione livello {level}")
            return temp_df
    print("[k-Anonymity] Could not achieve k-anonymity within generalization limits.")
    raise ValueError(f"Non è possibile ottenere k-anonimato per k={k} entro il livello {max_generalization}") #da decidere se lanciare un'eccezione o fare una print
    #return df