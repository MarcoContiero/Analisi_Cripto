def analizza_multi_timeframe(risultati_per_timeframe):
    """
    Analizza la coerenza tra 1H, 4H e 1D per assegnare un punteggio multi-timeframe.
    """
    scenari_rilevanti = {}
    for r in risultati_per_timeframe:
        tf = r.get("timeframe")
        if tf in ["1h", "4h", "1d"]:
            scenari_rilevanti[tf] = r.get("scenario_finale")

    scenari = list(scenari_rilevanti.values())
    scenario_unico = None
    punteggio = 0

    if all(s == "long" for s in scenari):
        scenario_unico = "long"
        punteggio = 15
    elif all(s == "short" for s in scenari):
        scenario_unico = "short"
        punteggio = 15
    elif scenari.count("long") >= 2:
        scenario_unico = "long"
        punteggio = 10
    elif scenari.count("short") >= 2:
        scenario_unico = "short"
        punteggio = 10
    else:
        scenario_unico = "neutro"
        punteggio = 2  # divergenza totale

    return {
        "indicatore": "multi_timeframe",
        "timeframes_considerati": scenari_rilevanti,
        "scenario": scenario_unico,
        "punteggio": punteggio
    }
