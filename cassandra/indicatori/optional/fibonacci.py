import pandas as pd


def analizza_fibonacci(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza i livelli di Fibonacci (ritracciamenti + estensioni).
    """
    max_swing = df["high"].rolling(window=100).max().iloc[-1]
    min_swing = df["low"].rolling(window=100).min().iloc[-1]
    prezzo_attuale = df["close"].iloc[-1]

    range_swing = max_swing - min_swing
    if range_swing == 0:
        return {
            "indicatore": "Fibonacci",
            "timeframe": timeframe,
            "scenario": "neutro",
            "punteggio": 0,
            "valore": prezzo_attuale,
            "messaggio": "Range swing nullo"
        }

    retracements = {
        0.236: max_swing - range_swing * 0.236,
        0.382: max_swing - range_swing * 0.382,
        0.5: max_swing - range_swing * 0.5,
        0.618: max_swing - range_swing * 0.618,
        0.786: max_swing - range_swing * 0.786,
        0.886: max_swing - range_swing * 0.886,
    }

    extensions = {
        1.272: max_swing + range_swing * 0.272,
        1.414: max_swing + range_swing * 0.414,
        1.618: max_swing + range_swing * 0.618,
        2.0: max_swing + range_swing * 1.0,
        2.618: max_swing + range_swing * 1.618,
        -1.272: min_swing - range_swing * 0.272,
        -1.414: min_swing - range_swing * 0.414,
        -1.618: min_swing - range_swing * 0.618,
    }

    def is_near(valore, target, tolleranza=range_swing * 0.015):
        return abs(valore - target) <= tolleranza

    # Verifica ritracciamenti
    for livello, target in retracements.items():
        if is_near(prezzo_attuale, target):
            if livello in [0.618, 0.786, 0.886]:
                scenario = "long" if prezzo_attuale > target else "short"
                return {
                    "indicatore": "Fibonacci",
                    "timeframe": timeframe,
                    "valore": round(prezzo_attuale, 2),
                    "scenario": scenario,
                    "punteggio": 5,
                    "messaggio": f"Ritracciamento su livello {livello}"
                }
            elif livello in [0.382, 0.5, 0.236]:
                return {
                    "indicatore": "Fibonacci",
                    "timeframe": timeframe,
                    "valore": round(prezzo_attuale, 2),
                    "scenario": "neutro",
                    "punteggio": 2,
                    "messaggio": f"Ritracciamento su livello {livello}"
                }

    # Verifica estensioni
    for livello, target in extensions.items():
        if is_near(prezzo_attuale, target):
            if livello > 0:
                return {
                    "indicatore": "Fibonacci",
                    "timeframe": timeframe,
                    "valore": round(prezzo_attuale, 2),
                    "scenario": "long",
                    "punteggio": 5,
                    "messaggio": f"Estensione long su livello {livello}"
                }
            else:
                return {
                    "indicatore": "Fibonacci",
                    "timeframe": timeframe,
                    "valore": round(prezzo_attuale, 2),
                    "scenario": "short",
                    "punteggio": 5,
                    "messaggio": f"Estensione short su livello {abs(livello)}"
                }

    return {
        "indicatore": "Fibonacci",
        "timeframe": timeframe,
        "valore": round(prezzo_attuale, 2),
        "scenario": "neutro",
        "punteggio": 0,
        "messaggio": "Nessun livello Fibonacci significativo"
    }
