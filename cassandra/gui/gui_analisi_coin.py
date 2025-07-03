import streamlit as st
from analisi.analizza_coin import analizza_coin

def interfaccia_analisi_coin():
    st.subheader("🔎 Analisi tecnica di una coin")

    nome_coin = st.text_input("Nome coin (es. BTCUSDT)", value="BTCUSDT")

    if st.button("Esegui analisi"):
        with st.spinner("Analisi in corso..."):
            try:
                risultato = analizza_coin(nome_coin)

                st.success("✅ Analisi completata")

                # Scenario finale
                finale = risultato.get("scenario_finale", {})
                st.markdown(f"**Scenario finale:** `{finale.get('scenario')}`")
                st.markdown(f"**Punteggio totale:** `{finale.get('punteggio_totale')}`")
                st.markdown(f"**Direzione:** `{finale.get('direzione')}`")

                # Multi-timeframe
                multi = risultato.get("multi_timeframe", {})
                st.markdown("---")
                st.markdown("📊 **Analisi multi-timeframe**")
                st.markdown(f"- Scenario: `{multi.get('scenario')}`")
                st.markdown(f"- Punteggio: `{multi.get('punteggio')}`")
                st.markdown(f"- Timeframes considerati: `{multi.get('timeframes_considerati')}`")

                # Riassunto testuale (se presente)
                if "riassunto_testuale" in risultato:
                    st.markdown("---")
                    st.markdown("📝 **Riassunto analisi:**")
                    st.text(risultato["riassunto_testuale"])

            except Exception as e:
                st.error(f"❌ Errore durante l'analisi: {e}")
