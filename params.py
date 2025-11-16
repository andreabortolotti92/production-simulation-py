
import numpy as np            # libreria per numeri casuali e calcoli numerici
import pandas as pd           # libreria per strutture tabellari (DataFrame)
from constants import *       # importa tutte le costanti del modulo constants.py

def set_seed(seed = DEFAULT_SEED):
    """Imposta il seed nella funzione random, per garantire il requisito della riproducibilità"""
    np.random.seed(seed)
    

def _rand_int(low, high):
    """Restituisce un intero casuale compreso tra low e high (entrambi inclusi)"""
    return int(np.random.randint(low, high + 1))


def generate_parameters(PRODUCTS):
    """Genera i parametri casuali per ciascun prodotto e la capacità totale giornaliera. """
    rows= []
    for name in sorted(PRODUCTS):
        #Genero i valori pseudocasuali di quantità, tempi e capacità
        lot_qty = _rand_int(*LOT_QTY_RANGE) #l'asterisco prima della costante impone l'unpacking della stessa
        unit_time = _rand_int(*UNIT_TIME_RANGE_MIN)
        daily_capacity = _rand_int(*DAILY_CAP_BY_PRODUCT_RANGE)

        #Eseguo l'append dei valori appena calcolati nella lista
        rows.append({
            "product": name,
            "lot_qty": lot_qty,
            "unit_time": unit_time,
            "daily_capacity": daily_capacity,
        })

    #Creo il DataFrame in Pandas
    params_df = pd.DataFrame(rows, columns=["product", "lot_qty", "unit_time", "daily_capacity"])

    # Capacità complessiva giornaliera del reparto (in minuti)
    daily_capacity_total = _rand_int(*DAILY_CAP_TOTAL_RANGE)

    return params_df, daily_capacity_total

