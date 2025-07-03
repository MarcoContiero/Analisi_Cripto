def analizza_rsi(df, timeframe):
    try:
        # Calcolo RSI
        rsi_value = ...  # calcolo vero qui
        # Logica per punteggio e scenario
        return {
            "indicatore": "RSI",
            "timeframe": timeframe,
            "scenario": "long",  # o altro
            "punteggio": 10,
            "valore": rsi_value,
            "messaggio": ""
        }
    except Exception as e:
        return {
            "indicatore": "RSI",
            "timeframe": timeframe,
            "scenario": "neutro",
            "punteggio": 0,
            "valore": None,
            "messaggio": f"Errore interno RSI: {e}"
        }
