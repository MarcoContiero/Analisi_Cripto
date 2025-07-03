def calcola_entry_stop_target(direzione: str, prezzo_corrente: float, volatilita: float = 0.02) -> dict:
    """
    Calcola entry, stop e target basati su direzione e volatilità stimata.

    Args:
        direzione (str): "long" o "short"
        prezzo_corrente (float): prezzo attuale dell'asset
        volatilita (float): percentuale stimata di movimento (default 2%)

    Returns:
        dict: valori entry, stop, target
    """
    if direzione == "long":
        entry = prezzo_corrente
        stop = round(entry * (1 - volatilita), 2)
        target = round(entry * (1 + 2 * volatilita), 2)
    elif direzione == "short":
        entry = prezzo_corrente
        stop = round(entry * (1 + volatilita), 2)
        target = round(entry * (1 - 2 * volatilita), 2)
    else:
        return {}

    return {
        "entry": round(entry, 2),
        "stop": stop,
        "target": target
    }
