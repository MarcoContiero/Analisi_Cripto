import pandas as pd
import ta.volatility


def analizza_bollinger(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza la posizione del prezzo rispetto alle bande di Bollinger.
    """
    bb = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2)
    upper = bb.bollinger_hband()
    lower = bb.bollinger_lband()
    mid = bb.bollinger_mavg()
    
    prezzo = df["close"].iloc[-1]
    spread = upper.iloc[-1] - lower.iloc[-1]
    squeeze = spread / mid.iloc[-1] < 0.05

    scenario = "neutro"
    punteggio = 2

    if prezzo > upper.iloc[-1]:
        scenario = "long"
        punteggio = 10
    elif prezzo < lower.iloc[-1]:
        scenario = "short"
        punteggio = 10
    elif squeeze:
        scenario = "potenziale breakout"
        punteggio = 8
    elif abs(prezzo - mid.iloc[-1]) < spread * 0.1:
        scenario = "nessuna direzione"
        punteggio = 4

    return {
        "indicatore": "Bollinger Bands",
        "timeframe": timeframe,
        "valore": round(prezzo, 2),
        "scenario": scenario,
        "punteggio": punteggio
    }
