import pandas as pd

def analizza_massimi_minimi(df: pd.DataFrame, timeframe: str, lookback: int = 50):
    """
    Analizza massimi e minimi su una finestra di lookback.
    Ritorna:
    - massimo e minimo assoluti
    - posizione (in candele fa)
    - breakout attivo (bool)
    - punteggio tecnico
    """
    massimo = df["high"].rolling(lookback).max().iloc[-1]
    minimo = df["low"].rolling(lookback).min().iloc[-1]
    
    massimo_idx = df["high"].iloc[-lookback:].idxmax()
    minimo_idx = df["low"].iloc[-lookback:].idxmin()
    
    ultimo_close = df["close"].iloc[-1]
    breakout_alto = ultimo_close > massimo
    breakout_basso = ultimo_close < minimo

    punteggio = 0
    if breakout_alto:
        punteggio += 3
    elif breakout_basso:
        punteggio += 3
    else:
        punteggio += 1  # neutro ma utile

    return {
        "indicatore": "massimi_minimi",
        "timeframe": timeframe,
        "massimo": round(massimo, 4),
        "minimo": round(minimo, 4),
        "massimo_n_candele_fa": len(df) - df.index.get_loc(massimo_idx),
        "minimo_n_candele_fa": len(df) - df.index.get_loc(minimo_idx),
        "breakout_alto": breakout_alto,
        "breakout_basso": breakout_basso,
        "punteggio": punteggio,
        "scenario": "long" if breakout_alto else "short" if breakout_basso else "neutro"
    }
