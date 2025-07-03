import ephem
from datetime import datetime

def analizza_fasi_lunari(df, timeframe):
    oggi = datetime.utcnow()
    fase_luna = ephem.Moon(oggi).phase  # 0 = Luna Nuova, 100 = Luna Piena

    if fase_luna < 7:
        scenario = "🌑⬆️"  # Storicamente mercato tende a salire con Luna Nuova
        messaggio = "Luna Nuova – storicamente associata a rialzi"
    elif fase_luna > 93:
        scenario = "🌕⬇️"  # Storicamente mercato tende a scendere con Luna Piena
        messaggio = "Luna Piena – storicamente associata a ribassi"
    else:
        scenario = "🌗"  # Quarti o fasi intermedie
        messaggio = "Fase intermedia – nessuna direzione storica prevalente"

    return {
        "indicatore": "Fasi Lunari",
        "timeframe": timeframe,
        "scenario": scenario,
        "messaggio": messaggio,
        "punteggio": 0
    }
