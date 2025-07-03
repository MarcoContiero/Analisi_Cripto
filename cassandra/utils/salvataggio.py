# utils/salvataggio.py

import os

def salva_analisi_completa(coin, risultato):
    """
    Ritorna una stringa formattata con:
    - valori indicatori per timeframe
    - punteggi per timeframe
    - osservazioni e conclusioni
    """
    scenario = risultato["scenario_finale"]
    dettagli = risultato["dettagli_per_timeframe"]
    riass_tecnico = risultato["riassunto_tecnico"]
    riass_globale = risultato["riassunto_testuale"]
    punteggi = risultato["punteggi_per_timeframe"]

    righe = [
        "# === INFO GENERALI ===",
        f"Coin: {coin}",
        f"Prezzo: {scenario['prezzo']}",
        f"Scenario finale: {scenario['direzione']}",
        f"Punteggio totale: {scenario['punteggio_totale']}",
        f"Timeframe dominante: {scenario['timeframe_dominante']}",
        ""
    ]

    righe.append("# === PUNTEGGI PER TIMEFRAME ===")
    for tf in ["1w","1d","4h","1h","15m"]:
        if tf in punteggi:
            sc = punteggi[tf]
            direz = scenario.get("direzioni", {}).get(tf, "neutro")
            righe.append(f"{tf}: {sc} ({direz})")
    righe.append("")

    righe.append("# === DETTAGLI INDICATORI PER TIMEFRAME ===")
    for tf in ["1w","1d","4h","1h","15m"]:
        righe.append(f"\n[{tf}]")
        for nome, info in dettagli.get(tf, {}).items():
            val = info.get("valore", "N/A")
            stz = info.get("scenario", "neutro")
            righe.append(f"{nome}: {val} ({stz})")
    righe.append("")

    righe.append("# === OSSERVAZIONI TECNICHE ===")
    righe.append(riass_tecnico.strip())
    righe.append("")

    righe.append("# === CONCLUSIONE GLOBALE ===")
    righe.append(riass_globale.strip())

    return "\n".join(righe)
