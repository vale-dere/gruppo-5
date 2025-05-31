import pandas as pd # Gestione data frame
import numpy as np  # Per il rumore casuale
from datetime import datetime # Per la gestione delle date

# Classe per Laplace
class Laplace:
    def __init__(self, epsilon, sensitivity=1):
        self.epsilon = epsilon
        self.sensitivity = sensitivity

    def randomise(self, value):
        scale = self.sensitivity / (self.epsilon + 1e-10)
        noise = np.random.laplace(0, scale)
        return value + noise

def apply_differential_privacy(df: pd.DataFrame, epsilon: float) -> pd.DataFrame:
    df_copy = df.copy() # Copio il data frame per non modificare l'originale
    
    for col in df.columns: # Scorro tutte le colonne del DataFrame per decidere l'approccio migliore per il tipo di dato
        col_data = df[col]
        
        # Se la colonna è numerica:
        if pd.api.types.is_numeric_dtype(col_data):
            # Calcola sensitivity dinamica (range massimo-minimo della colonna)
            col_min, col_max = col_data.min(), col_data.max()
            sensitivity = col_max - col_min if col_max != col_min else 1 # Se tutti i valori sono uguali restituiamo 1
            
            # Creo meccanismo Laplace e aggiungo rumore
            mech = Laplace(epsilon=epsilon, sensitivity=sensitivity)
            df_copy[col] = col_data.apply(lambda x: x + mech.randomise(0))
        
        # Se la colonna è una data:
        elif pd.api.types.is_datetime64_any_dtype(col_data):
            # Applica rumore sui secondi delle date (per preservare la granularità)
            seconds_noise = lambda d: d + pd.to_timedelta(np.random.laplace(scale=1/epsilon), unit='s') if pd.notnull(d) else d
            df_copy[col] = col_data.apply(seconds_noise)
        
        # Se la colonna è booleana:
        elif pd.api.types.is_bool_dtype(col_data):
            # Maschera booleani invertendo casualmente con probabilità controllata
            flip_prob = min(0.5, 1 / (epsilon + 1e-6))
            df_copy[col] = col_data.apply(lambda x: not x if np.random.rand() < flip_prob else x)
        
        # Se la colonna è testuale o categorica:
        else:
            # Pseudonimizzazione parziale dei testi
            def mask_text(val):
                if pd.isnull(val):
                    return val
                val_str = str(val)
                if len(val_str) <= 2: # Se la stringa è corta, maschera tutto
                    return '*' * len(val_str)
                return val_str[0] + '*' * (len(val_str)-2) + val_str[-1] # Altrimenti mostra prima e ultima lettera e maschera il resto
            
            df_copy[col] = col_data.apply(mask_text)
    
    return df_copy