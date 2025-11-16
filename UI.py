import os
from constants import DEFAULT_WIDTH

def clear_console():
    """Pulisce il terminale, funziona a prescindere dal sistema operativo"""
    if os.name == "nt": os.system("cls") 
    else: os.system("clear")
    
def wait():
    """Attende per permettere la lettura dei risultati, per procedere premere invio"""
    try:
        input("\nPremi Invio per continuare...")
    except KeyboardInterrupt:
        print("\nEsecuzione interrotta dall’utente.")

def wait_and_clear():
    """Combinazione di wait e clear_console"""
    wait()
    clear_console()

def _print_header(title, width = DEFAULT_WIDTH, char = "="):
    print(f"{char} {title} {char}".center(width + len(char)*2, char))

def _print_breaker(width = DEFAULT_WIDTH):
    print(f"=" * width)

def _normalize_and_measure(content):
    # Ritorna (lista_righe, larghezza_massima)
    if isinstance(content, str):
        lines = content.splitlines() or [content]
    elif isinstance(content, (list, tuple)):
        lines = [str(x) for x in content]
    else:
        text = str(content)
        lines = text.splitlines() or [text]
    max_width = max((len(line) for line in lines), default=0)
    return lines, max_width

def print_paragraph(title,content, char ="="):
    lines, max_width = _normalize_and_measure(content)
    _print_header(title, max_width, char)
    for line in lines:
        print(line)
    _print_breaker(max_width)
    print()

def prompt_seed(current_seed, default_seed):
    """Chiede l'inserimento di un seed intero"""
    clear_console()
    shown_seed = current_seed if current_seed is not None else default_seed

    title=("INSERIMENTO DEL SEED")
    content=("Inserisci un seed numerico per la simulazione. A parità di seed le esecuzioni daranno risultati identici.")
    content=content + (f"\nInserire un numero intero (oppure premere Invio per mantenere il seed corrente ({shown_seed})) ")
    print_paragraph(title, content)
    user_input = input("Inserisci il seed: ").strip()
    try:
        if 0 <= int(user_input) <= 2**32 - 1:
            print(f"Seed aggiornato ---> {int(user_input)}")
            wait_and_clear()
            return int(user_input) if user_input else int(shown_seed)
        else:
            print(f"Valore non valido (NumPy accetta solo valori da 0 a 2^32-1). Mantengo il seed precedente ({shown_seed}).")
            wait_and_clear()
            return int(shown_seed)
    except ValueError:
        print(f"Valore non valido. Mantengo il seed precedente ({shown_seed}).")
        wait_and_clear()
        return int(shown_seed)

def print_menu(seed, width = DEFAULT_WIDTH):
    """Stampa il menu principale"""
    print("\n" + "=" * width)
    print(" MENU PRINCIPALE — Digita il numero e premi Invio")
    print("-" * width)
    print(f"[1] Esegui flusso completo (seed → parametri → simulazione → KPI/tabelle)")
    if seed is not None:
        print(f"[2] Inserisci/modifica seed e genera parametri di lavorazione degli articoli  (seed impostato: {seed})")
    else:
        print("[2] Inserisci/modifica seed e genera parametri di lavorazione degli articoli")
    print("[3] Simula piano (richiede parametri)")
    print("[4] Mostra KPI e tabelle (richiede piano)")
    print("[Q] Esci")
    print("=" * width)
