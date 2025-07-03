import pandas as pd


def analizza_volume(df: pd.DataFrame, timeframe: str) -> dict:
    """
    Analizza il volume in relazione al movimento del prezzo.
    """
    vol = df["volume"]
    prezzo = df["close"]

    vol_now = vol.iloc[-1]
    vol_prev = vol.iloc[-2]
    delta_prezzo = prezzo.iloc[-1] - prezzo.iloc[-2]

    scenario = "neutro"
    punteggio = 2

    if vol_now > vol_prev:
        if delta_prezzo > 0:
            scenario = "long"
            punteggio = 8 if vol_now < vol.max() else 10
        elif delta_prezzo < 0:
            scenario = "short"
            punteggio = 8 if vol_now < vol.max() else 10
    elif vol_now < vol.mean():
        scenario = "flat"
        punteggio = 2

    return {
        "indicatore": "Volume",
        "timeframe": timeframe,
        "valore": round(vol_now, 2),
        "scenario": scenario,
        "punteggio": punteggio
    }
