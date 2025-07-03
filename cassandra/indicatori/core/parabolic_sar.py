import pandas as pd
import ta.trend


def analizza_parabolic_sar(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza la posizione del Parabolic SAR rispetto al prezzo.
    """
    sar = ta.trend.PSARIndicator(high=df["high"], low=df["low"], close=df["close"]).psar()
    prezzo = df["close"].iloc[-1]
    sar_val = sar.iloc[-1]
    sar_prev = sar.iloc[-2]

    scenario = "neutro"
    punteggio = 0

    if sar_prev > prezzo and sar_val < prezzo:
        scenario = "long (inversione)"
        punteggio = 3
    elif sar_prev < prezzo and sar_val > prezzo:
        scenario = "short (inversione)"
        punteggio = 3
    elif sar_val < prezzo:
        scenario = "long"
        punteggio = 5
    elif sar_val > prezzo:
        scenario = "short"
        punteggio = 5

    return {
        "indicatore": "Parabolic SAR",
        "timeframe": timeframe,
        "valore": round(sar_val, 2),
        "scenario": scenario,
        "punteggio": punteggio
    }
