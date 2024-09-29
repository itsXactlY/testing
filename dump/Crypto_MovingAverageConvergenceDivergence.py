from fastquant import get_crypto_data, backtest
crypto = get_crypto_data("BTC/USDT", "2023-12-01", "2024-12-31")
backtest('macd', crypto, fast_period=12, slow_period=26, signal_period=9, sma_period=30, dir_period=10)