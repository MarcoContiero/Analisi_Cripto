import pandas as pd


def analizza_ciclo(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza la fase del ciclo sulla base dei minimi locali.
    """
    chiusure = df["close"]
    prezzo_attuale = chiusure.iloc[-1]

    # Trova minimo locale negli ultimi 50 periodi
    minimo_recenti = chiusure.rolling(window=5, center=True).min()
    indice_minimi = minimo_recenti[minimo_recenti == chiusure].dropna().index

    if len(indice_minimi) == 0:
        return {
            "indicatore": "Ciclica",
            "timeframe": timeframe,
            "valore": prezzo_attuale,
            "scenario": "neutro",
            "punteggio": 0,
            "messaggio": "Nessun minimo locale rilevante"
        }

    ultimo_minimo_idx = indice_minimi[-1]
    distanza = len(chiusure) - ultimo_minimo_idx - 1

    if distanza <= 3:
        scenario = "long"
        punteggio = 5
        messaggio = "Inizio nuovo ciclo"
    elif distanza >= 15:
        scenario = "short"
        punteggio = 5
        messaggio = "Fase finale del ciclo"
    else:
        scenario = "neutro"
        punteggio = 3
        messaggio = "Fase intermedia del ciclo"

    return {
        "indicatore": "Ciclica",
        "timeframe": timeframe,
        "valore": prezzo_attuale,
        "scenario": scenario,
        "punteggio": punteggio,
        "messaggio": messaggio
    }
