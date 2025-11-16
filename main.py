from constants import PRODUCTS, DEFAULT_SEED
from params import set_seed, generate_parameters
from schedule import simulate_daily_schedule
from report import summarize, make_tables
from UI import *
from datetime import datetime

def show_params(seed, params_df, daily_capacity_total):
    """Funzione che stampa a schermo i parametri generati in precedenza"""
    print_paragraph("ORARIO ESECUZIONE", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print_paragraph("SEED", f"Il seed utilizzato è: {seed}")
    print_paragraph("PARAMETRI GENERATI",params_df.to_string(index=False))
    print_paragraph("CAPACITA' COMPLESSIVA",f"Capacità complessiva giornaliera (in minuti): {daily_capacity_total}")

def run_simulation(params_df, daily_capacity_total):
    """Funzione che esegue una simulazione, con l'obiettivo di produrre l'intero lotto di particolari generati"""
    plan_df = simulate_daily_schedule(params_df, daily_capacity_total)
    if plan_df.empty:
        print("\nATTENZIONE: il piano giornaliero è vuoto. Verificare i range in constants.py o la logica di schedule.py.")
    else:
        print_paragraph("PIANO GIORNALIERO", plan_df.to_string(index=False))
    return plan_df

def show_kpis(plan_df, params_df, daily_capacity_total):
    """Funzione che espone i KPI generati"""
    summary = summarize(plan_df, daily_capacity_total)
    tables = make_tables(plan_df, params_df, daily_capacity_total)

    print_paragraph("RIEPILOGO PER PRODOTTO",tables["product_summary_df"].to_string(index=False))
    print_paragraph("RIEPILOGO PER GIORNO",tables["day_summary_df"].to_string(index=False))
    print_paragraph("KPI SINTETICI", 
                    "\n".join([
                        f"Giorni totali: {summary['total_days']}",
                        f"Minuti allocati totali: {summary['total_minutes']}",
                        f"Utilizzo medio giornaliero (%): {None if summary['avg_daily_utilization'] is None else round(summary['avg_daily_utilization'], 2)}",
                        f"Lotti completati: {'Sì' if summary['completed_all'] else 'No'}",
                        ])
    )

def ensure_params(params_df, daily_capacity_total):
    """Verifica che ci siano i prerequisiti per lanciare l'opzione 3"""
    if params_df is None or daily_capacity_total is None:
        print("Parametri mancanti. Eseguire prima l'opzione [2] Genera parametri.")
        wait_and_clear()
        return False
    return True

def ensure_plan(plan_df, params_df, daily_capacity_total):
    """Verifica che ci siano i prerequisiti per lanciare l'opzione 4"""
    if plan_df is None or params_df is None or daily_capacity_total is None:
        print("Dati insufficienti. Eseguire prima [1] o [3].")
        wait_and_clear()
        return False
    return True

def main() -> None:
    clear_console()

    # Reset variabili
    seed, params_df, daily_capacity_total, plan_df, tables, summary = (None,) * 6

    while True:
        print_menu(seed)
        choice = input("Scelta: ").strip().lower()
        clear_console()

        if choice == "q":
            print("Chiusura programma.\n")
            break

        elif choice == "1":
            # Flusso completo
            seed = prompt_seed(seed, DEFAULT_SEED)
            set_seed(seed)

            params_df, daily_capacity_total = generate_parameters(PRODUCTS)
            show_params(seed, params_df, daily_capacity_total)
            wait()

            plan_df = run_simulation(params_df, daily_capacity_total)
            show_kpis(plan_df, params_df, daily_capacity_total)

            print("\nEsecuzione completata.\n")
            wait_and_clear()

        elif choice == "2":
            # Solo generazione parametri
            seed = prompt_seed(seed, DEFAULT_SEED)
            set_seed(int(seed))
            params_df, daily_capacity_total = generate_parameters(PRODUCTS)
            show_params(seed, params_df, daily_capacity_total)
            wait_and_clear()

        elif choice == "3":
            # Solo simulazione
            if not ensure_params(params_df, daily_capacity_total):
                continue
            plan_df = run_simulation(params_df, daily_capacity_total)
            wait_and_clear()

        elif choice == "4":
            # Solo KPI/tabelle
            if not ensure_plan(plan_df, params_df, daily_capacity_total):
                continue
            show_kpis(plan_df, params_df, daily_capacity_total)
            wait_and_clear()

        else:
            print("Funzionalità non trovata, riprovare.")
            wait_and_clear()

if __name__ == "__main__":
    main()
