import pandas as pd
import logging
from tools.hierarchy_builders import get_builder_for_column

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

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

def is_k_anonymous(df: pd.DataFrame, quasi_identifiers: list[str], k: int) -> bool:
    """Check if dataframe satisfies k-anonymity."""
    groups = df.groupby(quasi_identifiers).size()
    return (groups >= k).all()


def apply_k_anonymity(df: pd.DataFrame, quasi_identifiers: list, k: int) -> pd.DataFrame:
    """Apply k-anonymity via generalization of quasi-identifiers."""
    # Load hierarchies for each quasi-identifier
    hierarchies = {}
    
    for attr in quasi_identifiers:
        values = df[attr].dropna().astype(str).unique()

        # Use the dynamic function to get the builder, passing df for intelligent fallbacks
        builder = get_builder_for_column(attr, df)

        if builder:
            hierarchies[attr] = builder(values)
        else:
            # This should not happen with get_builder_for_column
            raise NotImplementedError(f"No hierarchy builder defined for QI: {attr}")
    max_level = 5  # generalization level, adjust as needed
    for level in range(max_level + 1):
        levels = {qi: level for qi in quasi_identifiers}
        df_gen = apply_generalization(df, quasi_identifiers, levels, hierarchies)
        if is_k_anonymous(df_gen, quasi_identifiers, k):
            logger.info(f"[k-Anonymity] Raggiunto con generalizzazione livello {level}")
            return df_gen

    raise ValueError("Could not satisfy k-anonymity with current hierarchies or levels.")
