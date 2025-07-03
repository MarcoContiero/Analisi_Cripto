def calcola_scenario_finale(risultati_per_timeframe):
    """
    Aggrega i punteggi dei vari timeframe e restituisce lo scenario dominante.
    """
    punteggi = {}
    direzioni = {}
    totale = 0
    conta = 0

    for blocco in risultati_per_timeframe:
        tf = blocco.get("timeframe")
        score = 0
        long_votes = 0
        short_votes = 0

        for indicatore in blocco.get("core", []) + blocco.get("optional", []):
            if indicatore is None:
                continue
            score += indicatore.get("punteggio", 0)
            if indicatore.get("scenario") == "long":
                long_votes += 1
            elif indicatore.get("scenario") == "short":
                short_votes += 1

        direzione = "long" if long_votes > short_votes else "short" if short_votes > long_votes else "neutro"
        media_score = round(score / max(1, len(blocco.get("core", []) + blocco.get("optional", []))), 2)

        punteggi[tf] = media_score
        direzioni[tf] = direzione
        totale += media_score
        conta += 1

    punteggio_totale = round(totale / max(1, conta), 2)

    # Determina timeframe dominante (quello con score massimo)
    if punteggi:
        tf_dominante = max(punteggi.items(), key=lambda x: x[1])[0]
        scenario = direzioni.get(tf_dominante, "neutro")
    else:
        tf_dominante = "1d"
        scenario = "neutro"

    # Preleva prezzo (dalla prima riga utile)
    prezzo = None
    for blocco in risultati_per_timeframe:
        df = blocco.get("df")
        if df is not None and not isinstance(df, str) and not df.empty:
            prezzo = round(float(df["close"].iloc[-1]), 4)
            break

    soglia_long = 0  # Puoi cambiarla in base a quanto "ottimista" vuoi essere

    return {
        "scenario": scenario,
        "punteggio_totale": punteggio_totale,
        "punteggi": punteggi,
        "timeframe_dominante": tf_dominante,
        "prezzo": prezzo,
        "direzione": "long" if punteggio_totale >= soglia_long else "short"
    }
