import os
import requests
import pandas as pd
from datetime import datetime

def scarica_ohlcv_binance(symbol: str, interval: str, limit: int = 1000, base_dir: str = "dati_csv"):
    """
    Scarica dati OHLCV dal public API di Binance e salva in CSV.
    """
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"❌ Errore API {symbol} @ {interval}: {response.text}")
        return

    data = response.json()
    if not data:
        print(f"❌ Nessun dato ricevuto per {symbol} @ {interval}")
        return

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df = df[["timestamp", "open", "high", "low", "close", "volume"]]
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    os.makedirs(base_dir, exist_ok=True)
    path = os.path.join(base_dir, f"{symbol}_{interval}.csv")
    df.to_csv(path, sep=";", decimal=",", index=False)
    print(f"✅ Salvato: {path}")

def scarica_tutti_tf(symbol: str, base_dir: str = "dati_csv"):
    """
    Scarica tutti i timeframe per una coin.
    """
    timeframe_list = ["15m", "1h", "4h", "1d", "1w"]
    for tf in timeframe_list:
        scarica_ohlcv_binance(symbol, tf, base_dir=base_dir)
