# analisi/valuta_indicatori.py

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

from indicatori.extra.fasi_lunari import analizza_fasi_lunari
from indicatori.extra.ichimoku import analizza_ichimoku
from indicatori.extra.adx import analizza_adx

def valuta_indicatori(df, timeframe):
    risultati = []

    # Indicatori core
    risultati.append(analizza_rsi(df, timeframe))
    risultati.append(analizza_macd(df, timeframe))
    risultati.append(analizza_ema(df, timeframe))
    risultati.append(analizza_bollinger(df, timeframe))
    risultati.append(analizza_parabolic_sar(df, timeframe))
    risultati.append(analizza_volume(df, timeframe))

    # Optional
    risultati.append(analizza_pattern_tecnici(df, timeframe))
    risultati.append(analizza_fvg(df, timeframe))
    risultati.append(analizza_gann(df, timeframe))
    risultati.append(analizza_fibonacci(df, timeframe))
    risultati.append(analizza_ciclo(df, timeframe))

    # Extra (senza punteggio)
    risultati.append(analizza_fasi_lunari(df, timeframe))
    risultati.append(analizza_ichimoku(df, timeframe))
    risultati.append(analizza_adx(df, timeframe))

    punteggio_long = 0
    punteggio_short = 0
    alert_visivi = []

    for r in risultati:
        scenario = r.get("scenario")
        punti = r.get("punteggio", 0)

        if scenario == "long":
            punteggio_long += punti
        elif scenario == "short":
            punteggio_short += punti

        if "🌑" in r.get("messaggio", "") or "🌕" in r.get("messaggio", ""):
            alert_visivi.append(r["messaggio"])

    scenario_finale = (
        "long" if punteggio_long > punteggio_short
        else "short" if punteggio_short > punteggio_long
        else "neutro"
    )

    return {
        "timeframe": timeframe,
        "punteggio_long": punteggio_long,
        "punteggio_short": punteggio_short,
        "scenario": scenario_finale,
        "dettagli": risultati,
        "alert_visivi": alert_visivi
    }
