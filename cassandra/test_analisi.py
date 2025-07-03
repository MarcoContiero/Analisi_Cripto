from analisi.analizza_coin import analizza_coin

def test_analizza_coin():
    nome_coin = "BTCUSDT"
    print(f"Avvio test analisi per {nome_coin}...")

    risultato = analizza_coin(nome_coin)

    print("Scenario finale:", risultato.get("scenario_finale"))
    print("Multi-timeframe:", risultato.get("multi_timeframe"))
    print("Numero timeframe analizzati:", len(risultato.get("analisi", [])))

    # Controllo base su presenza campo log
    assert "scenario_finale" in risultato, "Manca scenario finale"
    assert len(risultato["analisi"]) > 0, "Nessun risultato su timeframe"

    print("Test completato con successo.")

if __name__ == "__main__":
    test_analizza_coin()
