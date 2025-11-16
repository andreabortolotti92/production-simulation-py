# Interi
DEFAULT_SEED = 3753092  # seed predefinito per garantire riproducibilità
DEFAULT_WIDTH = 100 # larghezza di default per gestione interfaccia

# Set
PRODUCTS = {
    "Trave HEA100 tagliata a misura e forata",
    "Mensola fresata e forata",
    "Ante di chiusura",
    "Cancello carrabile",
    "Struttura metallica di supporto",
}

# Tuple - usate per definire range per la generazione casuale dei parametri
LOT_QTY_RANGE = (10, 50)                     # pezzi per prodotto
UNIT_TIME_RANGE_MIN = (30, 120)              # minuti per pezzo
DAILY_CAP_BY_PRODUCT_RANGE = (600, 2400)     # minuti/giorno per prodotto
DAILY_CAP_TOTAL_RANGE = (4800, 9600)         # minuti/giorno complessivi
