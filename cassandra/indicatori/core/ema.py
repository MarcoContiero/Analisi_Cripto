import pandas as pd
import ta.trend


def analizza_ema(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza la posizione del prezzo rispetto a EMA 9/21/50/200.
    """
    close = df["close"]
    ema9 = ta.trend.EMAIndicator(close, window=9).ema_indicator()
    ema21 = ta.trend.EMAIndicator(close, window=21).ema_indicator()
    ema50 = ta.trend.EMAIndicator(close, window=50).ema_indicator()
    ema200 = ta.trend.EMAIndicator(close, window=200).ema_indicator()
    
    prezzo = close.iloc[-1]
    valori = [ema9.iloc[-1], ema21.iloc[-1], ema50.iloc[-1], ema200.iloc[-1]]

    sopra_tutte = all(prezzo > ema for ema in valori)
    sotto_tutte = all(prezzo < ema for ema in valori)

    scenario = "neutro"
    punteggio = 5

    if sopra_tutte:
        scenario = "long"
        punteggio = 10
    elif sotto_tutte:
        scenario = "short"
        punteggio = 10
    elif prezzo < ema200.iloc[-1] < ema50.iloc[-1]:
        scenario = "short"
        punteggio = 8
    elif prezzo > ema200.iloc[-1] > ema50.iloc[-1]:
        scenario = "long"
        punteggio = 8

    return {
        "indicatore": "EMA",
        "timeframe": timeframe,
        "valore": round(prezzo, 2),
        "scenario": scenario,
        "punteggio": punteggio
    }
