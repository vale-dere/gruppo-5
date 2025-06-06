import pandas as pd
import numpy as np
from scipy.stats import wasserstein_distance

def calculate_distribution(series: pd.Series) -> pd.Series:
    """
    Calcola la distribuzione normalizzata degli elementi in una Series.
    Se non è possibile ordinare gli indici (tipi non confrontabili),
    restituisce la distribuzione così com’è.
    """
    dist = series.value_counts(normalize=True)
    try:
        dist = dist.sort_index()
    except (TypeError, KeyError):
        pass
    return dist

def distribution_distance(dist1: pd.Series, dist2: pd.Series) -> float:
    """
    Calcola la Earth Mover's Distance (Wasserstein) tra due distribuzioni discrete.
    Trasforma tutti gli indici in stringhe per ordinarli senza errori di confronto.
    """
    all_vals_raw = set(dist1.index).union(dist2.index)
    all_vals = sorted(str(v) for v in all_vals_raw)

    p = np.array([dist1.get(val, 0) for val in all_vals], dtype=float)
    q = np.array([dist2.get(val, 0) for val in all_vals], dtype=float)

    # Se entrambe le distribuzioni sono tutte zero, la distanza è zero
    if np.allclose(p.sum(), 0) and np.allclose(q.sum(), 0):
        return 0.0

    # Normalizza per sicurezza (devono sommare a 1)
    if not np.isclose(p.sum(), 1.0):
        p = p / p.sum() if p.sum() > 0 else np.ones_like(p) / len(p)
    if not np.isclose(q.sum(), 1.0):
        q = q / q.sum() if q.sum() > 0 else np.ones_like(q) / len(q)

    positions = np.arange(len(p))
    return wasserstein_distance(positions, positions, p, q)

def apply_t_closeness(
    df: pd.DataFrame,
    quasi_ids: list,
    sensitive_attr: str,
    t: float,
    random_state: int = 42
) -> pd.DataFrame:
    """
    Applica t-Closeness al DataFrame `df`, raggruppando secondo `quasi_ids` e
    proteggendo l'attributo sensibile `sensitive_attr`.

    Ogni gruppo la cui distanza dalla distribuzione globale supera `t`
    sostituisce **per forza** ogni valore “sensitive” con un nuovo valore
    diverso estratto dalla distribuzione globale (escludendo l’originale),
    in modo che quel gruppo diventi esattamente equivalente alla distribuzione globale.
    """
    np.random.seed(random_state)
    df_copy = df.copy()

    # 1) Forza tutti i valori “sensitive” a stringhe (evitiamo tipi misti)
    df_copy[sensitive_attr] = df_copy[sensitive_attr].astype(str)

    # 2) Calcola distribuzione globale su sensitive_attr
    global_dist = calculate_distribution(df_copy[sensitive_attr])
    if global_dist.isnull().any() or not np.isfinite(global_dist.values).all():
        raise ValueError("Distribuzione globale contiene NaN o infiniti.")
    if np.isclose(global_dist.sum(), 0.0):
        raise ValueError("Distribuzione globale risulta con somma zero.")
    global_dist = global_dist / global_dist.sum()

    # 3) Se c’è un MultiIndex, facciamo reset_index per manipolare più agevolmente
    had_multiindex = isinstance(df_copy.index, pd.MultiIndex)
    if had_multiindex:
        df_copy = df_copy.reset_index()

    # 4) Raggruppa per quasi-identifiers, senza droppare eventuali NA nei QI
    grouped = df_copy.groupby(quasi_ids, dropna=False)
    modified_groups = []

    for _, group_df in grouped:
        current_df = group_df.copy()

        # 4.1) Calcola distribuzione “sensitive” del gruppo e distanza globale
        group_dist = calculate_distribution(current_df[sensitive_attr])
        dist = distribution_distance(global_dist, group_dist)

        # 4.2) Se la distanza supera t, sostituisci ogni riga “sensitive”
        if dist > t:
            for idx in current_df.index:
                orig_val = current_df.at[idx, sensitive_attr]
                # Distr globale temporanea: metti peso 0 all’originale e poi ribilancia
                temp_dist = global_dist.copy()
                if orig_val in temp_dist.index:
                    temp_dist[orig_val] = 0.0
                temp_dist = temp_dist / temp_dist.sum()
                new_val = np.random.choice(temp_dist.index, p=temp_dist.values)
                current_df.at[idx, sensitive_attr] = new_val

        modified_groups.append(current_df)

    # 5) Ricompone il DataFrame anonimo
    result_df = pd.concat(modified_groups)

    # 6) Se avevamo fatto reset_index, ripristiniamo il MultiIndex originale
    if had_multiindex:
        result_df = result_df.set_index(df.index.names)

    # 7) Riordiniamo le righe come nell’originale
    result_df = result_df.loc[df.index]

    return result_df