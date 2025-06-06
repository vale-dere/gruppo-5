import pandas as pd
import json
from tools.hierarchy_builders import get_builder_for_column

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
    #se non vengono trovati attributi sensibili, l'algoritmo non può essere applicato capisci se chiedere all'utente di specificarlo e aggiunerlo al momento oppure dare errore e basta (large.health file test)

    # Load hierarchies for each quasi-identifier
    hierarchies = {}
    
    for attr in quasi_identifiers:
        values = df[attr].dropna().astype(str).unique()

        # Usa la funzione dinamica per ottenere il builder, passandogli df per fallback intelligenti
        builder = get_builder_for_column(attr, df)

        if builder:
            hierarchies[attr] = builder(values)
        else:
            # Questo non dovrebbe mai succedere con get_builder_for_column
            raise NotImplementedError(f"No hierarchy builder defined for QI: {attr}")

    max_level = 5  # adjust as needed
    for level in range(max_level + 1):
        levels = {qi: level for qi in quasi_identifiers}
        df_gen = apply_generalization(df, quasi_identifiers, levels, hierarchies)
        groups = df_gen.groupby(quasi_identifiers)
        if all(is_l_diverse(group, sensitive_attr, l) for _, group in groups):
            print(f"Achieved l-diversity with generalization level {level} for l={l}")
            return df_gen
        print(f"\nGeneralization level {level}")
        print(df_gen)

    raise ValueError("Could not satisfy l-diversity with current hierarchies or levels.")     

    '''
    -After grouping by generalized QIs, we check each group for l-diversity.
    -If a group does not satisfy l-diversity, it is suppressed (excluded).
    -Suppressed rows count is printed to monitor how many records are removed.
    -Once a generalization level results in no suppression, it means all groups satisfy l-diversity → return generalized dataset.
    -If no generalization level can satisfy l-diversity without suppression, a ValueError is raised.

    def apply_l_diversity(df: pd.DataFrame, quasi_identifiers: list, sensitive_attr: list, l: int) -> pd.DataFrame:
    """
    Applies l-diversity to the dataset by progressively generalizing QIs.
    Groups that do not satisfy l-diversity after generalization are suppressed (removed).
    
    Args:
        df: Original DataFrame
        quasi_identifiers: List of quasi-identifier columns
        sensitive_attr: List of sensitive attribute columns to check diversity on
        l: Desired level of l-diversity (minimum distinct sensitive values per group)
        
    Returns:
        A new DataFrame generalized and suppressed to satisfy l-diversity.
    """
    hierarchies = {}
    for attr in quasi_identifiers:
        values = df[attr].dropna().astype(str).unique()
        builder = get_builder_for_column(attr, df)
        if builder:
            hierarchies[attr] = builder(values)
        else:
            raise NotImplementedError(f"No hierarchy builder defined for QI: {attr}")

    max_level = 5  # Max generalization level to try

    for level in range(max_level + 1):
        levels = {qi: level for qi in quasi_identifiers}
        df_gen = apply_generalization(df, quasi_identifiers, levels, hierarchies)

        groups = df_gen.groupby(quasi_identifiers)

        # Keep groups that satisfy l-diversity
        diverse_groups = []
        suppressed_count = 0

        for _, group in groups:
            if is_l_diverse(group, sensitive_attr, l):
                diverse_groups.append(group)
            else:
                suppressed_count += len(group)  # Count suppressed rows

        if diverse_groups:
            # Concatenate only diverse groups, effectively suppressing others
            result_df = pd.concat(diverse_groups, ignore_index=True)
        else:
            result_df = pd.DataFrame(columns=df.columns)  # No groups passed

        print(f"Generalization level {level} - suppressed rows: {suppressed_count}")

        # If no rows were suppressed, l-diversity is satisfied for all
        if suppressed_count == 0:
            print(f"Achieved l-diversity with generalization level {level} for l={l}")
            return result_df

    raise ValueError("Could not satisfy l-diversity with current hierarchies or levels.")
    '''

#per ora il mio algoritmo generalizza tutto e anche troppo, per generalizzare meno andrebbero implementate delle tecniche tipo quella di mondrian
#ma potrebbe essere tr5oppo complicato. il codice commentato di sopra dovrebbe creare delle partizioni in modo tale che ci possono essere vari sottogruppi
#a livello diverso, ma che in generale poi ispettano tutti i livello richiesto
 