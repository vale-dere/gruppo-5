import pandas as pd
import numpy as np
from scipy.stats import entropy
from collections import Counter

def calculate_distribution(column):
    """Calcola la distribuzione normalizzata per una colonna."""
    counts = Counter(column.dropna())
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}

def kl_divergence(p_dist, q_dist):
    """Calcola la divergenza Kullback-Leibler tra due distribuzioni."""
    p = np.array([p_dist.get(k, 1e-10) for k in q_dist.keys()])
    q = np.array([q_dist.get(k, 1e-10) for k in q_dist.keys()])
    return entropy(p, q)

def apply_t_closeness(df: pd.DataFrame, sensitive_cols: list, t: float, group_col=None) -> pd.DataFrame:
    df_copy = df.copy()

    # Distribuzioni globali delle colonne sensibili
    global_distributions = {col: calculate_distribution(df[col]) for col in sensitive_cols}
    
    if group_col is None:
        # Se non si specifica un group_col, applica pseudonimizzazione "globale" per ridurre la distanza
        for col in sensitive_cols:
            col_data = df[col]
            most_common = col_data.mode().iloc[0] if not col_data.mode().empty else None
            
            # Maschera o sostituisci i valori con i più comuni per avvicinare le distribuzioni
            df_copy[col] = col_data.apply(
                lambda x: most_common if kl_divergence(
                    calculate_distribution(pd.Series([x])),
                    global_distributions[col]
                ) > t else x
            )
    else:
        # Raggruppa per group_col e controlla t-closeness
        grouped = df.groupby(group_col)
        for name, group in grouped:
            for col in sensitive_cols:
                local_dist = calculate_distribution(group[col])
                divergence = kl_divergence(local_dist, global_distributions[col])
                
                if divergence > t:
                    # Maschera o sostituisci valori per ridurre la distanza
                    most_common = df[col].mode().iloc[0] if not df[col].mode().empty else None
                    indices = group.index
                    df_copy.loc[indices, col] = group[col].apply(lambda x: most_common)
    
    return df_copy
