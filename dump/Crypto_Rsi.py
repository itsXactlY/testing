from fastquant import get_crypto_data, backtest
crypto = get_crypto_data("BTC/USDT", "2018-12-01", "2019-12-31")
backtest('rsi', crypto, rsi_period=14, rsi_upper=70, rsi_lower=30)
