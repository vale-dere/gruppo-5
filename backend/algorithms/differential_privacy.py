import pandas as pd
import numpy as np

class Laplace:
    def __init__(self, epsilon, sensitivity=1.0):
        self.epsilon = epsilon
        self.sensitivity = sensitivity

    def noise(self, size):
        scale = self.sensitivity / (self.epsilon + 1e-10)
        return np.random.laplace(loc=0.0, scale=scale, size=size)

def randomized_response_categorical(series, epsilon):
    """
    Applica randomized response per dati categorici:
    Con probabilità p = e^ε / (e^ε + k - 1) mantieni il valore originale,
    altrimenti scegli randomicamente uno dei valori possibili (escluso il valore originale).
    """
    values = series.dropna().unique()
    k = len(values)
    if k <= 1:
        return series  # Se c'è un solo valore, niente da privatizzare

    exp_eps = np.exp(epsilon)
    p = exp_eps / (exp_eps + k - 1)

    def privatize_value(val):
        if np.random.rand() < p:
            return val
        else:
            other_vals = [v for v in values if v != val]
            return np.random.choice(other_vals)

    return series.apply(privatize_value)

def apply_differential_privacy(df: pd.DataFrame, epsilon: float) -> pd.DataFrame:
    df_copy = df.copy()

    for col in df.columns:
        col_data = df[col]

        # Numeric columns
        if pd.api.types.is_numeric_dtype(col_data):
            col_min = col_data.min()
            col_max = col_data.max()
            sensitivity = max(col_max - col_min, 1.0)
            mech = Laplace(epsilon, sensitivity)
            noise = mech.noise(len(col_data))
            df_copy[col] = col_data + noise

        # Datetime columns
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            timestamps = col_data.astype(np.int64) / 1e9  # Convert to seconds
            ts_min = timestamps.min()
            ts_max = timestamps.max()
            sensitivity = max(ts_max - ts_min, 1.0)
            mech = Laplace(epsilon, sensitivity)
            noisy_ts = timestamps + mech.noise(len(col_data))
            df_copy[col] = pd.to_datetime(noisy_ts, unit='s')

        # Boolean columns
        elif pd.api.types.is_bool_dtype(col_data):
            flip_prob = min(0.5, 1 / (epsilon + 1e-6))
            flips = np.random.rand(len(col_data)) < flip_prob
            df_copy[col] = col_data ^ flips  # XOR: True <-> False

        # Categorical/Textual columns
        else:
            df_copy[col] = randomized_response_categorical(col_data.fillna(''), epsilon)

    return df_copy
