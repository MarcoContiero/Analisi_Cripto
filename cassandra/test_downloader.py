import ccxt
import pandas as pd
import os

exchange = ccxt.binance()

def get_ohlcv_binance(symbol, timeframe, limit=1000):
    """
    Scarica dati OHLCV da Binance per una determinata coppia e timeframe.
    """
    data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    return df

def salva_csv(df, nome_file):
    """
    Salva il DataFrame su file CSV con separatore ; e virgola decimale.
    """
    df.to_csv(nome_file, sep=";", decimal=",")
    print(f"✅ Dati salvati in {nome_file}")

def scarica_tutti_tf(symbol, base_dir="dati_csv", limit=1000):
    """
    Scarica tutti i timeframe definiti e salva in CSV.
    """
    os.makedirs(base_dir, exist_ok=True)
    timeframe_list = ["15m", "1h", "4h", "1d", "1w"]
    for tf in timeframe_list:
        print(f"📥 Scarico {symbol} @ {tf}...")
        df = get_ohlcv_binance(symbol, tf, limit)
        filename = os.path.join(base_dir, f"{symbol.replace('/', '')}_{tf}.csv")
        salva_csv(df, filename)
