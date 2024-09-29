from fastquant import get_crypto_data, backtest
crypto = get_crypto_data("BTC/USDT", "2018-12-01", "2019-12-31")
backtest('smac', crypto, fast_period=15, slow_period=40)