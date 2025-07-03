import pandas as pd
import ta.trend


def analizza_macd(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza il MACD sul dataframe fornito e restituisce punteggio e scenario.
    """
    macd_indicator = ta.trend.MACD(close=df['close'])
    macd_line = macd_indicator.macd()
    signal_line = macd_indicator.macd_signal()
    macd_hist = macd_indicator.macd_diff()

    # Prendiamo gli ultimi 3 valori per valutare incroci o tendenze
    macd_now = macd_line.iloc[-1]
    signal_now = signal_line.iloc[-1]
    hist_now = macd_hist.iloc[-1]

    macd_prev = macd_line.iloc[-2]
    signal_prev = signal_line.iloc[-2]
    hist_prev = macd_hist.iloc[-2]

    # Default
    scenario = "neutro"
    punteggio = 2

    # Detect incrocio rialzista con istogramma crescente
    if macd_prev < signal_prev and macd_now > signal_now and hist_now > hist_prev:
        scenario = "long"
        punteggio = 10

    # Detect incrocio ribassista con istogramma decrescente
    elif macd_prev > signal_prev and macd_now < signal_now and hist_now < hist_prev:
        scenario = "short"
        punteggio = 10

    # MACD sopra zero ma piatto
    elif macd_now > 0 and abs(hist_now) < 0.1:
        scenario = "neutro"
        punteggio = 6

    # MACD sotto zero e decrescente
    elif macd_now < 0 and hist_now < hist_prev:
        scenario = "short"
        punteggio = 7

    return {
        "indicatore": "MACD",
        "timeframe": timeframe,
        "valore": round(macd_now, 4),
        "scenario": scenario,
        "punteggio": punteggio
    }
