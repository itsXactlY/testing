from fastquant import backtest, get_database_stock_data
data = get_database_stock_data("EUR_USD", "2020-01-01", "2024-01-01", "1m")
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