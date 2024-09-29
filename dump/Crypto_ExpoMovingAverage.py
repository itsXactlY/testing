from fastquant import get_crypto_data, backtest
crypto = get_crypto_data("BTC/USDT", "2018-12-01", "2019-12-31")
backtest('emac', crypto, fast_period=10, slow_period=30)