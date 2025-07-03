import pandas as pd

def analizza_fvg(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza la presenza di Fair Value Gaps (FVG) recenti e assegna scenario e punteggio.
    Cerca gap tra la candela n-2 e n.
    """

    if len(df) < 3:
        return {
            "indicatore": "FVG",
            "timeframe": timeframe,
            "scenario": "neutro",
            "messaggio": "Dati insufficienti",
            "punteggio": 0
        }

    candle_2 = df.iloc[-3]
    candle_1 = df.iloc[-2]
    candle_0 = df.iloc[-1]

    # Fair Value Gap: high di -2 < low di 0 → gap rialzista
    if candle_2['high'] < candle_0['low']:
        scenario = "long"
        descrizione = f"FVG rialzista: gap tra {round(candle_2['high'], 2)} e {round(candle_0['low'], 2)}"
        punteggio = 5

    # Fair Value Gap: low di -2 > high di 0 → gap ribassista
    elif candle_2['low'] > candle_0['high']:
        scenario = "short"
        descrizione = f"FVG ribassista: gap tra {round(candle_0['high'], 2)} e {round(candle_2['low'], 2)}"
        punteggio = 5

    else:
        scenario = "neutro"
        descrizione = "Nessun FVG significativo"
        punteggio = 0

    return {
        "indicatore": "FVG",
        "timeframe": timeframe,
        "scenario": scenario,
        "messaggio": descrizione,
        "punteggio": punteggio
    }
