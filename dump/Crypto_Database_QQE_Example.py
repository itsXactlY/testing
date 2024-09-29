from fastquant import get_database_data, backtest
data = get_database_data("BTC/USDT", "2020-01-01", "2024-01-01", "1m")
backtest('OrChainKioseff', 
        data, 
        init_cash=1000,
        take_profit_percent=2,
        dca_deviation=1.5,
        percent_sizer=0.3,
        backtest=True)

'''    
OrChainKioseff
msa
STScalp
'''