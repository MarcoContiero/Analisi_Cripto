import pandas as pd
import numpy as np

def analizza_gann(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza l'interazione del prezzo con gli angoli di Gann.
    Usa 5 angoli base: 1:1, 2:1, 1:2, 4:1, 1:4 e valuta il comportamento del prezzo.
    """
    # Prendiamo il primo punto disponibile per ancorare gli angoli
    base_time = df['timestamp'].iloc[0]
    base_price = df['close'].iloc[0]

    # Calcola numero totale di candele
    num_candele = len(df)

    # Crea scala tempo/prezzo
    scale_ratio = (df['close'].max() - df['close'].min()) / num_candele
    scale_ratio = scale_ratio if scale_ratio != 0 else 1

    # Definizione angoli Gann
    angoli = {
        '1:1': 1,
        '2:1': 2,
        '1:2': 0.5,
        '4:1': 4,
        '1:4': 0.25
    }

    punteggio = 0
    scenario = "neutro"
    messaggi = []

    for nome, rapporto in angoli.items():
        linea = []
        for i in range(num_candele):
            prezzo_linea = base_price + (i * scale_ratio * rapporto)
            linea.append(prezzo_linea)
        df[f'gann_{nome}'] = linea

        # Confronta prezzo attuale con linea Gann
        prezzo_attuale = df['close'].iloc[-1]
        linea_attuale = linea[-1]

        diff_percentuale = (prezzo_attuale - linea_attuale) / linea_attuale * 100

        if abs(diff_percentuale) <= 0.5:
            punteggio = max(punteggio, 2)
            scenario = "neutro"
            messaggi.append(f"Prezzo vicino all'angolo {nome}")
        elif diff_percentuale > 1:
            punteggio = max(punteggio, 5)
            scenario = "long"
            messaggi.append(f"Breakout sopra angolo {nome}")
        elif diff_percentuale < -1:
            punteggio = max(punteggio, 5)
            scenario = "short"
            messaggi.append(f"Breakdown sotto angolo {nome}")

    return {
        "indicatore": "Gann",
        "timeframe": timeframe,
        "scenario": scenario,
        "punteggio": punteggio,
        "messaggio": "; ".join(messaggi)
    }
