from analisi.analizza_coin import analizza_coin
from utils.salvataggio import salva_analisi_completa

def genera_classifica(lista_coin, soglia=0):
    classifica = []
    for coin in lista_coin:
        try:
            risultato = analizza_coin(coin)
            if not risultato:
                print(f"⚠️ Nessun risultato per {coin}, salto.")
                continue

            punteggio_totale = risultato["scenario_finale"].get("punteggio_totale", 0)
            if punteggio_totale < soglia:
                print(f"⚠️ {coin} scartata per punteggio {punteggio_totale} < soglia {soglia}")
                continue

            # Calcolo punteggi per timeframe
            punteggi_per_tf = {}
            for r in risultato.get("analisi", []):
                tf = r.get("timeframe")
                core = r.get("core", [])
                punteggi_per_tf[tf] = sum(ind.get("punteggio", 0) for ind in core if ind)

            # Passa il dizionario esteso a salva_analisi_completa
            risultato_esteso = {
                **risultato,
                "punteggi_per_timeframe": punteggi_per_tf
            }

            contenuto_file = salva_analisi_completa(coin, risultato_esteso)
            nome_file = f"analisi_{coin}.txt"
            with open(nome_file, "w", encoding="utf-8") as f:
                f.write(contenuto_file)

            entry = {
                "coin": coin,
                "score_15m": punteggi_per_tf.get("15m", 0),
                "score_1h": punteggi_per_tf.get("1h", 0),
                "score_4h": punteggi_per_tf.get("4h", 0),
                "score_1d": punteggi_per_tf.get("1d", 0),
                "score_1w": punteggi_per_tf.get("1w", 0),
                "score_totale": punteggio_totale,
                "direzione": risultato["scenario_finale"].get("direzione", "neutro"),
                "freccia": "⬆️" if risultato["scenario_finale"].get("direzione") == "long" else
                           "⬇️" if risultato["scenario_finale"].get("direzione") == "short" else "➡️",
                "file_analisi": nome_file
            }

            print(f"✅ {coin} aggiunta alla classifica con punteggio {punteggio_totale}")
            classifica.append(entry)

        except Exception as e:
            print(f"❌ Errore durante l'analisi di {coin}: {e}")
            continue

    return classifica
