import pandas as pd
import numpy as np
import logging
from tools.hierarchy_builders import get_builder_for_column

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

def calculate_distribution(series: pd.Series) -> pd.Series:
    dist = series.value_counts(normalize=True)
    try:
        dist = dist.sort_index()
    except (TypeError, KeyError):
        pass
    return dist

def distribution_distance(dist1: pd.Series, dist2: pd.Series) -> float:
    all_vals = set(dist1.index).union(dist2.index)
    
    p = np.array([dist1.get(val, 0) for val in all_vals], dtype=float)
    q = np.array([dist2.get(val, 0) for val in all_vals], dtype=float)

    # Normalize distributions if necessary
    if np.allclose(p.sum(), 0) and np.allclose(q.sum(), 0):
        return 0.0
    if not np.isclose(p.sum(), 1.0):
        p = p / p.sum() if p.sum() > 0 else np.ones_like(p) / len(p)
    if not np.isclose(q.sum(), 1.0):
        q = q / q.sum() if q.sum() > 0 else np.ones_like(q) / len(q)

    # L1 Distance (Total Variation Distance)
    return 0.5 * np.sum(np.abs(p - q))

def is_t_close(df: pd.DataFrame, quasi_ids: list, sensitive_attr: str, t: float) -> bool:
    global_dist = calculate_distribution(df[sensitive_attr])

    grouped = df.groupby(quasi_ids, dropna=False)
    for group_name, group_df in grouped:
        group_dist = calculate_distribution(group_df[sensitive_attr])
        dist = distribution_distance(global_dist, group_dist)
        logger.info(f"Group {group_name} - distance {dist:.4f}")
        if dist > t:
            return False
    return True

def apply_generalization(df, quasi_identifiers, gen_levels, hierarchies):
    df_copy = df.copy()
    for attr in quasi_identifiers:
        df_copy[attr] = df_copy[attr].astype(str).apply(
            lambda x: generalize_value(x, hierarchies[attr], gen_levels[attr])
        )
    return df_copy

def generalize_value(value: str, hierarchy: dict, levels: int) -> str:
    for _ in range(levels):
        if value not in hierarchy:
            break
        value = hierarchy[value]
    return value

def apply_t_closeness(df: pd.DataFrame, quasi_ids: list, sensitive_attr: str, t: float, max_generalization: int = 5) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy[sensitive_attr] = df_copy[sensitive_attr].astype(str)

    # Build hierarchies for quasi-identifiers
    hierarchies = {}
    for attr in quasi_ids:
        values = df_copy[attr].dropna().astype(str).unique()
        builder = get_builder_for_column(attr, df_copy)
        if builder:
            hierarchies[attr] = builder(values)
        else:
            raise NotImplementedError(f"No hierarchy builder available for {attr}")

    for level in range(max_generalization + 1):
        levels = {qi: level for qi in quasi_ids}
        df_gen = apply_generalization(df_copy, quasi_ids, levels, hierarchies)

        if is_t_close(df_gen, quasi_ids, sensitive_attr, t):
            logger.info(f"[t-Closeness] Achieved with generalization level {level}")
            return df_gen

        logger.info(f"[t-Closeness] Generalization level {level} not sufficient")

    raise ValueError(f"Cannot satisfy t-closeness with t={t} within the maximum generalization level {max_generalization}")