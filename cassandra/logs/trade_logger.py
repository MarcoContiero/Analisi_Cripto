# logs/trade_logger.py

import csv
import os
from datetime import datetime
import json

LOG_FILE = "logs/trades_log.csv"

def carica_log_giornaliero():
    oggi = datetime.utcnow().strftime("%Y-%m-%d")
    risultati = []
    if not os.path.exists(LOG_FILE):
        return risultati

    with open(LOG_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            if row.get("Data", "").startswith(oggi):
                risultati.append(row)
    return risultati

def salva_log_trade(riga):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_esiste = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "Data", "Coin", "Timeframe", "Punteggio Long", "Punteggio Short",
            "Scenario", "Entry", "Stop", "Target", "Score",
            "Entry TF", "TP raggiunto", "SL colpito", "Dettagli"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_esiste:
            writer.writeheader()
        writer.writerow(riga)

LOG_FILE = "logs/trades_log.csv"

def inizializza_log():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "Data", "Coin", "Timeframe", "Punteggio Long", "Punteggio Short", "Scenario",
                "Entry", "Stop", "Target", "Score", "Entry TF", "TP raggiunto", "SL colpito", "Dettagli"
            ])


LOG_FILE = "logs/trades_log.csv"

def logga_trade(
    coin: str,
    timeframe: str,
    punteggio_long: float,
    punteggio_short: float,
    scenario: str,
    entry: float,
    stop: float,
    target: float,
    score: float,
    dettagli: dict,
    entry_tf: str = "1h",
    tp_raggiunto: bool = False,
    sl_colpito: bool = False
):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_esiste = os.path.exists(LOG_FILE)

    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = [
            "Data", "Coin", "Timeframe", "Punteggio Long", "Punteggio Short",
            "Scenario", "Entry", "Stop", "Target", "Score", "Entry TF",
            "TP raggiunto", "SL colpito", "Dettagli"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_esiste:
            writer.writeheader()

        riga = {
            "Data": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
            "Coin": coin,
            "Timeframe": timeframe,
            "Punteggio Long": punteggio_long,
            "Punteggio Short": punteggio_short,
            "Scenario": scenario,
            "Entry": entry,
            "Stop": stop,
            "Target": target,
            "Score": score,
            "Entry TF": entry_tf,
            "TP raggiunto": int(tp_raggiunto),
            "SL colpito": int(sl_colpito),
            "Dettagli": json.dumps(dettagli, ensure_ascii=False)
        }

        writer.writerow(riga)


