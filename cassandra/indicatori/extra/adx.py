import pandas as pd
import ta.trend

def analizza_adx(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza l'indicatore ADX per valutare la forza del trend, senza punteggio.
    """
    df = df.copy()

    adx_indicator = ta.trend.ADXIndicator(
        high=df['high'], 
        low=df['low'], 
        close=df['close'], 
        window=14
    )

    adx = adx_indicator.adx().iloc[-1]
    messaggio = f"ADX = {round(adx, 2)} → "

    if adx >= 25:
        messaggio += "trend forte"
        scenario = "trend forte"
    elif 15 <= adx < 25:
        messaggio += "trend moderato"
        scenario = "moderato"
    else:
        messaggio += "assenza di trend"
        scenario = "debole"

    return {
        "indicatore": "ADX",
        "timeframe": timeframe,
        "scenario": scenario,
        "messaggio": messaggio,
        "punteggio": 0
    }
