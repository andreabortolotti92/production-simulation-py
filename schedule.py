import pandas as pd

def simulate_daily_schedule(params_df, daily_capacity_total):
    """Simula la produzione giorno per giorno rispettando i vincoli di capacità (totale di reparto e massima per prodotto)"""

    # Creo una copia del DataFrame params_df in p, ordinando il dato per prodotto e resettando l'indice
    # In questo modo si lavora su una copia e il DataFrame originale non subisce alterazioni
    p = (params_df.copy().sort_values("product").reset_index(drop=True))

    remaining = p.set_index("product")["lot_qty"].to_dict()             # Partendo da p creo un dizionario con indice product e valore di lot_qty
    cap_per_prod = p.set_index("product")["daily_capacity"].to_dict()   # Partendo da p creo un dizionario con indice product e valore di daily_capacity
    unit_time = p.set_index("product")["unit_time"].to_dict()           # Partendo da p creo un dizionario con indice product e valore di unit_time

    product_order = list(p["product"])
    rows = []
    day = 1

    # Funzione di controllo: vero se tutte le rimanenze sono 0
    def all_done(rem):
        return all(qty <= 0 for qty in rem.values())

    # Ciclo di N giorni (sicurezza su 10000), la condizione da verificare è che non siano esaurite tutte le quantità
    while not all_done(remaining):
        daily_total_left = daily_capacity_total  # inizializzo daily_total_left con la capacità giornaliera

        # Creo un dizionario temporaneo di giornata con le coppie prodotto - capacità giornaliera
        per_prod_left = {}
        for name in product_order:
            per_prod_left[name] = cap_per_prod[name] 

        # Ciclo sui prodotti in ordine alfabetico
        for name in product_order:
            if daily_total_left <= 0 or all_done(remaining):  #se ho terminato la capacità giornaliera totale oppure ho terminato i pezzi esce dal for
                break
            
            # assegno a rem_qty il valore residuo di tale prodotto
            rem_qty = remaining[name]

            # Se la quantità residua del prodotto è 0, passo all'iterazione (prodotto) successiva
            if rem_qty == 0:
                continue  

            # Minuti che posso allocare oggi a questo prodotto (minimo tra la capacità di produzione dello specifico articolo e quella giornaliera residua)
            alloc_cap = min(per_prod_left[name], daily_total_left)
            if alloc_cap <= 0:
                # Se l'allocazione per questo prodotto è <=0 passo all'iterazione successiva
                continue

            # Calcolo il numero di pezzi da poter produrre con i minuti allocabili
            ut = unit_time[name]
            max_pieces_today = alloc_cap // ut
            if max_pieces_today <= 0:
                # Se non basta per 1 pezzo, passo all'iterazione successiva
                continue

            # Max_pieces_today potrebbe essere più alto del residuo da produrre, calcolo il minimo tra i due valori
            produced = min(rem_qty, max_pieces_today)
            used_minutes = produced * ut

            # Aggiornamenti di stato dei dizionari/variabili
            remaining[name] -= produced
            per_prod_left[name] -= used_minutes
            daily_total_left -= used_minutes

            # Riga del piano giornaliero
            rows.append({
                "day": day,
                "product": name,
                "production_time": unit_time[name],
                "qty_to_product": rem_qty,
                "product_capacity": cap_per_prod[name],
                "daily_capacity": daily_total_left + used_minutes,
                "alloc_minutes": used_minutes,
                "produced_qty": produced,
                "remaining_qty": remaining[name],
            })

            #Se non ho più capienza esco dal for
            if daily_total_left <= 0:
                break 

        day += 1

        # Nel caso dovessi raggiungere un numero di giorni eccessivamente elevato, imposto una sicurezza
        if day > 10000:
            raise RuntimeError("La simulazione ha superato il limite di giorni previsto.")

    # A fine esecuzione creo un DataFrame Pandas per mostrare i risultati dell'elaborazione
    plan_df = pd.DataFrame(rows, columns=["day", "product", "production_time", "qty_to_product", "product_capacity", "daily_capacity", "alloc_minutes", "produced_qty", "remaining_qty"])
    
    if not plan_df.empty:
        plan_df.sort_values(["day", "product"], inplace=True, ignore_index=True)
    return plan_df


