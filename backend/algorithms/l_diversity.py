import pandas as pd
import json
from tools.hierarchy_builders import QI_HIERARCHY_BUILDERS

# Generalize values using the hierarchy
def generalize_value(value: str, hierarchy: dict, levels: int) -> str:
    """
    Applies a given number of generalization steps to a value using its hierarchy.
    If no more generalization is possible, returns the same value.
    """
    for _ in range(levels):
        if value not in hierarchy:
            break
        value = hierarchy[value]
    return value

# Apply generalization to the whole dataset
def apply_generalization(df, quasi_identifiers, gen_levels, hierarchies):
    """
    Applies generalization to all quasi-identifiers in the DataFrame.
    
    Args:
        df: Original DataFrame
        qi: List of quasi-identifier columns
        levels: Dictionary of generalization levels per column
        hierarchies: Dictionary of loaded hierarchies per column
        
    Returns:
        A new DataFrame with generalized quasi-identifiers
    """
    df_copy = df.copy()
    for attr in quasi_identifiers:
        df_copy[attr] = df_copy[attr].astype(str).apply(
            lambda x: generalize_value(x, hierarchies[attr], gen_levels[attr])
        )
    return df_copy

# Check if a group satisfies l-diversity
def is_l_diverse(group, sensitive_attrs, l):
    for attr in sensitive_attrs:
        if len(set(group[attr])) < l:
            return False
    return True

# Find the minimum level of generalization needed to satisfy l-diversity
def apply_l_diversity(df: pd.DataFrame, quasi_identifiers: list, sensitive_attr: list, l: int) -> pd.DataFrame:
    # Load hierarchies for each quasi-identifier
    hierarchies = {}
    for attr in quasi_identifiers:
        values = df[attr].dropna().astype(str).unique()
        builder = QI_HIERARCHY_BUILDERS.get(attr.lower()) # Get the hierarchy builder function for the attribute
        if builder:
            hierarchies[attr] = builder(values)
        else:
            raise NotImplementedError(f"No hierarchy builder defined for QI: {attr}")

    max_level = 3  # adjust as needed
    for level in range(max_level + 1):
        levels = {qi: level for qi in quasi_identifiers}
        df_gen = apply_generalization(df, quasi_identifiers, levels, hierarchies)
        groups = df_gen.groupby(quasi_identifiers)
        if all(is_l_diverse(group, sensitive_attr, l) for _, group in groups):
            print(f"Achieved l-diversity with generalization level {level} for l={l}")
            return df_gen

    raise ValueError("Could not satisfy l-diversity with current hierarchies or levels.")     
