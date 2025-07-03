import pandas as pd
import ta.trend

def analizza_ichimoku(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza l'indicatore Ichimoku (solo Kumo + Tenkan/Kijun) e restituisce uno scenario descrittivo.
    """
    df = df.copy()
    
    # Calcolo Ichimoku
    ichimoku = ta.trend.IchimokuIndicator(
        high=df['high'], 
        low=df['low'], 
        window1=9, 
        window2=26, 
        window3=52,
        fillna=True
    )
    
    df['tenkan'] = ichimoku.ichimoku_conversion_line()
    df['kijun'] = ichimoku.ichimoku_base_line()
    df['senkou_a'] = ichimoku.ichimoku_a()
    df['senkou_b'] = ichimoku.ichimoku_b()
    
    # Ultimo valore disponibile
    prezzo = df['close'].iloc[-1]
    tenkan = df['tenkan'].iloc[-1]
    kijun = df['kijun'].iloc[-1]
    senkou_a = df['senkou_a'].iloc[-1]
    senkou_b = df['senkou_b'].iloc[-1]

    kumo_high = max(senkou_a, senkou_b)
    kumo_low = min(senkou_a, senkou_b)

    if prezzo > kumo_high:
        scenario = "long"
        messaggio = "Prezzo sopra la Kumo (nuvola) → trend rialzista"
    elif prezzo < kumo_low:
        scenario = "short"
        messaggio = "Prezzo sotto la Kumo (nuvola) → trend ribassista"
    else:
        scenario = "neutro"
        messaggio = "Prezzo dentro la Kumo → fase di indecisione"

    if tenkan > kijun:
        messaggio += " | Tenkan > Kijun (supporto al long)"
    elif tenkan < kijun:
        messaggio += " | Tenkan < Kijun (supporto allo short)"
    else:
        messaggio += " | Tenkan ≈ Kijun"

    return {
        "indicatore": "Ichimoku",
        "timeframe": timeframe,
        "scenario": scenario,
        "messaggio": messaggio,
        "punteggio": 0
    }
