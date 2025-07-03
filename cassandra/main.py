import streamlit as st
import pandas as pd
import os
import glob
from analisi.analizza_coin import analizza_coin
from analisi.classifica_generator import genera_classifica
from utils.salvataggio import salva_analisi_completa

# === TITOLO ===
st.title("📊 Cassandra - Analisi Cripto Multi-Timeframe")

# === Soglia evidenziazione ===
soglia_alert = st.slider("🎯 Soglia punteggio per evidenziare (alert)", 0, 100, 70)

# === Caricamento lista da file ===
def carica_lista_coin():
    with open("config/lista_coin.txt", "r") as f:
        return [riga.strip().upper() for riga in f if riga.strip()]

# === ANALISI SINGOLA ===
st.subheader("🔎 Analizza una singola coin")
coin_singola = st.text_input("Inserisci la coin (es. ETHUSDT)")

if st.button("Analizza coin"):
    try:
        risultato = analizza_coin(coin_singola)
        st.success(f"✅ Analisi completata per {coin_singola}")

        st.markdown(f"**{coin_singola}** - `{risultato['scenario_finale']['direzione']}`")
        st.markdown(f"Punteggio: `{risultato['scenario_finale']['punteggio_totale']}` | TF dominante: `{risultato['scenario_finale']['timeframe_dominante']}`")
        st.markdown(f"Prezzo attuale: `{risultato['scenario_finale']['prezzo']}`")

        with st.expander("📌 Riassunto Tecnico"):
            st.text_area("📋 Riassunto tecnico", risultato["riassunto_tecnico"], height=300)

        with st.expander("📌 Riassunto Globale"):
            st.text_area("📋 Riassunto globale", risultato["riassunto_testuale"], height=300)

        # Scarica analisi singola (formato completo)
        contenuto_file = salva_analisi_completa(coin_singola, risultato)
        st.download_button(
            label=f"📄 Scarica analisi di {coin_singola}",
            data=contenuto_file.encode("utf-8"),
            file_name=f"analisi_{coin_singola}.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ Errore durante l'analisi di {coin_singola}: {e}")

# === CLASSIFICA COMPLETA ===
st.subheader("📈 Classifica Completa")

classifica = []

if st.button("🔄 Aggiorna classifica"):
    lista_coin = carica_lista_coin()
    classifica = genera_classifica(lista_coin, soglia=soglia_alert)

    if classifica:
        df_classifica = pd.DataFrame(classifica)
        df_classifica = df_classifica.sort_values(by="score_totale", ascending=False)

        st.markdown("## 🏆 Classifica Coin")

        # Intestazione tabella
        header_cols = st.columns([1.2,1,1,1,1,1,1,0.8,1.8,2])
        header_cols[0].markdown("**Coin**")
        header_cols[1].markdown("15m")
        header_cols[2].markdown("1h")
        header_cols[3].markdown("4h")
        header_cols[4].markdown("1d")
        header_cols[5].markdown("1w")
        header_cols[6].markdown("Totale")
        header_cols[7].markdown("Dir.")
        header_cols[8].markdown("📄 Tecnica")
        header_cols[9].markdown("🧠 Globale")

        # Riga per riga
        for _, row in df_classifica.iterrows():
            cols = st.columns([1.2,1,1,1,1,1,1,0.8,1.8,2])
            cols[0].markdown(f"**{row['coin']}**")
            cols[1].write(row['score_15m'])
            cols[2].write(row['score_1h'])
            cols[3].write(row['score_4h'])
            cols[4].write(row['score_1d'])
            cols[5].write(row['score_1w'])
            cols[6].write(row['score_totale'])
            cols[7].write(row['freccia'])

            # Pulsante download analisi tecnica
            if os.path.exists(row['file_analisi']):
                with open(row['file_analisi'], "rb") as f:
                    cols[8].download_button(
                        label="📄",
                        data=f,
                        file_name=row['file_analisi'],
                        mime="text/plain",
                        key=f"tec_{row['coin']}"
                    )
            else:
                cols[8].write("N/A")

            # Pulsante download analisi globale (per ora uguale a tecnica)
            if os.path.exists(row['file_analisi']):
                with open(row['file_analisi'], "rb") as f:
                    cols[9].download_button(
                        label="🧠",
                        data=f,
                        file_name=f"globale_{row['file_analisi']}",
                        mime="text/plain",
                        key=f"glob_{row['coin']}"
                    )
            else:
                cols[9].write("N/A")

        # Download classifica CSV
        csv = df_classifica.to_csv(index=False, sep=";", decimal=",").encode("utf-8")
        st.download_button(
            label="⬇️ Scarica classifica completa",
            data=csv,
            file_name="classifica_completa.csv",
            mime="text/csv"
        )

# === PULSANTE DOWNLOAD TUTTE LE ANALISI GLOBALI ===
import glob

if st.button("⬇️ Scarica tutte le analisi globali in un file"):
    percorso_file = "analisi_aggregate.txt"
    file_analisi_globale = glob.glob("analisi_globale_*.txt")

    contenuto_aggregato = ""
    for file_path in file_analisi_globale:
        with open(file_path, "r", encoding="utf-8") as f:
            contenuto_aggregato += f"=== Analisi {file_path} ===\n"
            contenuto_aggregato += f.read() + "\n\n"

    st.download_button(
        label="📥 Scarica file completo",
        data=contenuto_aggregato.encode("utf-8"),
        file_name=percorso_file,
        mime="text/plain"
    )
