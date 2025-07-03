import os
import pandas as pd
from indicatori.core.rsi import analizza_rsi
from indicatori.core.macd import analizza_macd
from indicatori.core.ema import analizza_ema
from indicatori.core.bollinger import analizza_bollinger
from indicatori.core.parabolic_sar import analizza_parabolic_sar
from indicatori.core.volume import analizza_volume
from indicatori.core.multi_timeframe import analizza_multi_timeframe
from indicatori.optional.pattern_tecnici import analizza_pattern_tecnici
from indicatori.optional.fvg import analizza_fvg
from indicatori.optional.gann_levels import analizza_gann
from indicatori.optional.fibonacci import analizza_fibonacci
from indicatori.optional.analisi_ciclica import analizza_ciclo
from indicatori.optional.massimi_minimi import analizza_massimi_minimi
from indicatori.extra.adx import analizza_adx
from indicatori.extra.ichimoku import analizza_ichimoku
from indicatori.extra.fasi_lunari import analizza_fasi_lunari
from indicatori.core.calcola_scenario_finale import calcola_scenario_finale
from logs.trade_logger import logga_trade
from entry_exit.calcola_entry_stop_target import calcola_entry_stop_target
from dati.downloader import scarica_tutti_tf  # aggiungi questo in cima al file, se non c'è già

# Timeframe in ordine di peso (dal più alto al più basso)
TIMEFRAMES = ["1w", "1d", "4h", "1h", "15m"]

def carica_dati(timeframe: str, nome_coin: str, path_base: str = "dati_csv"):
    nome_file = f"{nome_coin}_{timeframe}.csv"
    path_file = os.path.join(path_base, nome_file)
    if not os.path.exists(path_file):
        raise FileNotFoundError(f"❌ File non trovato: {path_file}")
    df = pd.read_csv(path_file, sep=';')
    df.columns = df.columns.str.lower()

    # Converti le colonne numeriche in float
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Converti timestamp in datetime (se serve)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    return df

def analizza_coin(nome_coin: str):
    scarica_tutti_tf(nome_coin)  # scarica tutti i timeframe se mancanti

    risultati = []

    for tf in TIMEFRAMES:
        try:
            df = carica_dati(tf, nome_coin)
            df.columns = df.columns.str.lower()

            core = [
                analizza_rsi(df, tf),
                analizza_macd(df, tf),
                analizza_ema(df, tf),
                analizza_bollinger(df, tf),
                analizza_parabolic_sar(df, tf),
                analizza_volume(df, tf),
            ]

            optional = [
                analizza_pattern_tecnici(df, tf),
                analizza_fvg(df, tf),
                analizza_gann(df, tf),
                analizza_fibonacci(df, tf),
                analizza_ciclo(df, tf),
                analizza_adx(df, tf),
                analizza_ichimoku(df, tf),
                analizza_fasi_lunari(df, tf),
                analizza_massimi_minimi(df, tf),
            ]

            risultati.append({
                "timeframe": tf,
                "core": core,
                "optional": optional,
                "df": df  # ✅ fondamentale per ottenere il prezzo
            })

        except Exception as e:
            print(f"⚠️ Errore analizzando {nome_coin} [{tf}]: {e}")

    print("=== DEBUG risultati per timeframe ===")
    for idx, r in enumerate(risultati):
        print(f"Timeframe #{idx} = {r.get('timeframe')}")
        core = r.get('core', [])
        for i, indicatore in enumerate(core):
            if indicatore is None:
                print(f"⚠️ Core indicatore #{i} è None")
            else:
                # Controlla campi importanti, ad esempio:
                if 'punteggio' not in indicatore or indicatore['punteggio'] is None:
                    print(f"⚠️ Core indicatore #{i} manca punteggio")
                if 'scenario' not in indicatore or indicatore['scenario'] is None:
                    print(f"⚠️ Core indicatore #{i} manca scenario")

        optional = r.get('optional', [])
        for i, indicatore in enumerate(optional):
            if indicatore is None:
                print(f"⚠️ Optional indicatore #{i} è None")
            else:
                if 'punteggio' not in indicatore or indicatore['punteggio'] is None:
                    print(f"⚠️ Optional indicatore #{i} manca punteggio")
                if 'scenario' not in indicatore or indicatore['scenario'] is None:
                    print(f"⚠️ Optional indicatore #{i} manca scenario")
    print("=== FINE DEBUG risultati ===")

    # Preparazione degli scenari per ogni singolo timeframe
    scenari_per_tf = []
    for r in risultati:
        core_clean = [x for x in r.get('core', []) if x is not None]
        punteggio_long = sum(i.get('punteggio', 0) for i in core_clean if i.get('scenario') == 'long')
        punteggio_short = sum(i.get('punteggio', 0) for i in core_clean if i.get('scenario') == 'short')
        # ...


        if punteggio_long > punteggio_short:
            scenario = 'long'
        elif punteggio_short > punteggio_long:
            scenario = 'short'
        else:
            scenario = 'neutro'

        scenari_per_tf.append({'timeframe': r.get('timeframe'), 'scenario': scenario})

    # Calcolo multi-timeframe
    try:
        multi = analizza_multi_timeframe(scenari_per_tf)
    except Exception as e:
        multi = {"indicatore": "Multi-timeframe", "scenario": "neutro", "punteggio": 0}
        print(f"⚠️ Errore nel calcolo multi-timeframe: {e}")

    # Calcolo scenario finale e score
    try:
        finale = calcola_scenario_finale(risultati)  # ✅ corretto: solo la lista dei risultati
    except Exception as e:
        finale = {"scenario": "errore", "punteggio_totale": 0, "direzione": "neutro"}
        print(f"⚠️ Errore nel calcolo dello scenario finale: {e}")

        # Dopo il calcolo dello scenario finale
    try:
        # Prendiamo il dataframe dell'ultimo timeframe (es. 1d) per entry/stop/target
        df_ultimo_tf = carica_dati("1d", nome_coin)
        df_ultimo_tf.columns = df_ultimo_tf.columns.str.lower()

        scenario_finale = finale.get("scenario", "neutro")

        if scenario_finale in ["long", "short"]:
            prezzo_corrente = df_ultimo_tf['close'].iloc[-1]
            result = calcola_entry_stop_target(scenario_finale, prezzo_corrente)

            entry = result['entry']
            stop = result['stop']
            target = result['target']

            punteggio_long = finale.get("punteggio_long", 0)
            punteggio_short = finale.get("punteggio_short", 0)
            score = max(punteggio_long, punteggio_short)

            dettagli_sintetici = {
                "scenario": finale.get("scenario"),
                "punteggio_totale": finale.get("punteggio_totale"),
                "direzione": finale.get("direzione"),
            }

            logga_trade(
                coin=nome_coin,
                timeframe="1d",
                punteggio_long=punteggio_long,
                punteggio_short=punteggio_short,
                scenario=scenario_finale,
                entry=entry,
                stop=stop,
                target=target,
                score=score,
                dettagli=dettagli_sintetici,
                entry_tf="1d"
            )


    except Exception as e:
        print(f"⚠️ Errore nel logging trade per {nome_coin}: {e}")

    

    riassunto_testuale = costruisci_riassunto_globale(risultati, multi, finale)

    # Costruisci il dizionario base
    risultato_finale = {
        "coin": nome_coin,
        "analisi": risultati,
        "multi_timeframe": multi,
        "scenario_finale": finale,
        "riassunto_testuale": riassunto_testuale,
        "risultati": risultati
    }

    # Costruisci dettagli_per_timeframe
    dettagli_per_timeframe = {}

    for r in risultati:
        tf = r["timeframe"]
        dettagli_per_timeframe[tf] = {}

        for indicatore in r.get("core", []) + r.get("optional", []):
            if indicatore is None:
                continue

            nome = indicatore.get("indicatore", "Sconosciuto")
            valore = indicatore.get("valore", "n/a")
            scenario = indicatore.get("scenario", "n/a")

            dettagli_per_timeframe[tf][nome] = {
                "valore": valore,
                "scenario": scenario
            }

    risultato_finale["dettagli_per_timeframe"] = dettagli_per_timeframe

    # Aggiungi il riassunto tecnico
    risultato_finale["riassunto_tecnico"] = genera_riassunto_tecnico(risultato_finale)

    return risultato_finale


def genera_riassunto_tecnico(risultati: dict) -> str:
    coin = risultati.get("coin", "N/A")
    analisi = risultati.get("analisi", [])
    multi = risultati.get("multi_timeframe", {})
    finale = risultati.get("scenario_finale", {})

    righe = []
    righe.append(f"📌 Coin: {coin}")
    righe.append("")

    for r in analisi:
        tf = r.get("timeframe", "N/A")
        righe.append(f"⏱ Timeframe: {tf}")

        for categoria in ["core", "optional"]:
            if r.get(categoria):
                righe.append(f"  🔹 {categoria.upper()}:")
                for ind in r[categoria]:
                    nome = ind.get("indicatore", "N/A")
                    scenario = ind.get("scenario", "N/A")
                    punteggio = ind.get("punteggio", 0)
                    righe.append(f"     - {nome}: {scenario} ({punteggio})")
        righe.append("")

    # Multi-timeframe
    righe.append("🔄 Multi-timeframe:")
    righe.append(f"     - Scenario: {multi.get('scenario', 'N/A')} ({multi.get('punteggio', 0)})")
    righe.append("")

    # Scenario finale
    righe.append("🎯 Scenario Finale:")
    righe.append(f"     - Direzione: {finale.get('direzione', 'N/A')}")
    righe.append(f"     - Punteggio Totale: {finale.get('punteggio_totale', 0)}")

    return "\n".join(righe)

def costruisci_riassunto_globale(analisi, multi, finale):
    righe = []
    righe.append(f"Analisi globale per coin: {finale.get('coin', 'N/A')}")
    righe.append(f"Scenario finale: {finale.get('scenario', 'neutro')} con punteggio totale {finale.get('punteggio_totale', 0)}")

    righe.append("\nPunteggi per timeframe:")
    for r in analisi:
        tf = r['timeframe']
        punteggio_core = sum(i['punteggio'] for i in r['core'])
        punteggio_optional = sum(i['punteggio'] for i in r['optional'])
        righe.append(f" - {tf}: Core={punteggio_core}, Optional={punteggio_optional}")

    righe.append(f"\nMulti-timeframe scenario: {multi.get('scenario', 'neutro')} con punteggio {multi.get('punteggio', 0)}")

    righe.append("\nConsiderazioni:")
    # Qui puoi aggiungere righe personalizzate in base a valori, es. se scenario è long ma punteggio basso ecc.
    if finale.get('scenario') == 'long' and finale.get('punteggio_totale', 0) < 50:
        righe.append(" - Segnale long ma con forza moderata, attenzione ai pullback.")
    elif finale.get('scenario') == 'short' and finale.get('punteggio_totale', 0) < 50:
        righe.append(" - Segnale short debole, confermare con altri indicatori.")
    else:
        righe.append(" - Segnale chiaro e robusto.")

    return "\n".join(righe)
