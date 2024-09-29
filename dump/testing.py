# As seen at: https://www.youtube.com/watch?v=M4s9ECVjM-8
# Intended for 15 second candle(s)
# Very raw prototype (yet)
import backtrader as bt
from fastquant.strategies.base import BaseStrategy, BuySellArrows
from GRID_DynamicFloating import DynamicGridStrategy
class AlligatorCCIAOStrategy(BaseStrategy):
    params = (
        ('jaw_period', 12),
        ('teeth_period', 7),
        ('lips_period', 6), 
        ('cci_period', 7),
        ('ao_period1', 7),
        ('ao_period2', 11),
        ('backtest', None)
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        BuySellArrows(self.data0, barplot=True)
        self.jaw = bt.indicators.SmoothedMovingAverage(self.data.close, period=self.params.jaw_period)
        self.teeth = bt.indicators.SmoothedMovingAverage(self.data.close, period=self.params.teeth_period)
        self.lips = bt.indicators.SmoothedMovingAverage(self.data.close, period=self.params.lips_period)
        self.cci = bt.indicators.CommodityChannelIndex(period=self.params.cci_period)
        self.ao = bt.indicators.AwesomeOscillator(self.data, fast=self.params.ao_period1, slow=self.params.ao_period2)

    def next(self):
        alligator_up = self.jaw > self.lips
        alligator_down = self.teeth < self.lips

        cci_up = self.cci > 80
        cci_down = self.cci < -80

        ao_up = self.ao[0] > self.ao[-1] > self.ao[-2] > 0
        ao_down = self.ao[0] < self.ao[-1] < self.ao[-2] < 0

        if alligator_up and cci_up and ao_up:
            if not self.position:
                self.buy(size=100)

        if alligator_down and cci_down and ao_down:
            if self.position:
                self.sell(size=100)

import backtrader.indicators as btind

class Accumulator(bt.Indicator):
    lines = ('acc',)
    params = (('seed', 1),)

    def __init__(self, condition, func):
        self.condition = condition
        self.func = func

    def next(self):
        if len(self) == 1:
            self.lines.acc[0] = self.p.seed
        else:
            if self.condition:
                self.lines.acc[0] = self.func(self.lines.acc[-1])
            else:
                self.lines.acc[0] = self.lines.acc[-1]


class RSX(bt.Indicator):
    lines = ('rsx',)
    params = (('length', 14), ('src', 'close'))

    def __init__(self):
        self.addminperiod(self.p.length)
        self.f8 = 100 * self.data.close
        self.f10 = self.f8(-1)
        self.v8 = self.f8 - self.f10

        self.f18 = 3 / (self.p.length + 2)
        self.f20 = 1 - self.f18

        self.f28 = btind.EMA(self.v8, period=self.p.length)
        self.f30 = btind.EMA(self.f28, period=self.p.length)
        self.vC = self.f28 * 1.5 - self.f30 * 0.5

        self.f38 = btind.EMA(self.vC, period=self.p.length)
        self.f40 = btind.EMA(self.f38, period=self.p.length)
        self.v10 = self.f38 * 1.5 - self.f40 * 0.5

        self.f48 = btind.EMA(self.v10, period=self.p.length)
        self.f50 = btind.EMA(self.f48, period=self.p.length)
        self.v14 = self.f48 * 1.5 - self.f50 * 0.5

        self.f58 = btind.EMA(abs(self.v8), period=self.p.length)
        self.f60 = btind.EMA(self.f58, period=self.p.length)
        self.v18 = self.f58 * 1.5 - self.f60 * 0.5

        self.f68 = btind.EMA(self.v18, period=self.p.length)
        self.f70 = btind.EMA(self.f68, period=self.p.length)
        self.v1C = self.f68 * 1.5 - self.f70 * 0.5

        self.f78 = btind.EMA(self.v1C, period=self.p.length)
        self.f80 = btind.EMA(self.f78, period=self.p.length)
        self.v20 = self.f78 * 1.5 - self.f80 * 0.5

        self.f88 = btind.If(self.f80 == 0, self.p.length - 1, 5)
        self.f90 = Accumulator(condition=self.f88 == self.f88(-1), func=lambda x: x + 1)

        self.v4 = btind.If(bt.And(self.f88 < self.f90, self.v20 > 0), (self.v14 / self.v20 + 1) * 50, 50)
        self.lines.rsx = btind.If(self.v4 > 100, 100, btind.If(self.v4 < 0, 0, self.v4))

class SuperTrend(bt.Indicator):
    lines = ('super_trend',)
    params = (('period', 7), ('multiplier', 3))

    def __init__(self):
        self.st = [0]
        self.finalupband = [0]
        self.finallowband = [0]
        self.addminperiod(self.p.period)
        atr = bt.ind.ATR(self.data, period=self.p.period)
        self.upperband = (self.data.high + self.data.low) / 2 + self.p.multiplier * atr
        self.lowerband = (self.data.high + self.data.low) / 2 - self.p.multiplier * atr

    def next(self):
        pre_upband = self.finalupband[0]
        pre_lowband = self.finallowband[0]
        if self.upperband[0] < self.finalupband[-1] or self.data.close[-1] > self.finalupband[-1]:
            self.finalupband[0] = self.upperband[0]
        else:
            self.finalupband[0] = self.finalupband[-1]
        if self.lowerband[0] > self.finallowband[-1] or self.data.close[-1] < self.finallowband[-1]:
            self.finallowband[0] = self.lowerband[0]
        else:
            self.finallowband[0] = self.finallowband[-1]
        if self.data.close[0] <= self.finalupband[0] and ((self.st[-1] == pre_upband)):
            self.st[0] = self.finalupband[0]
            self.lines.super_trend[0] = self.finalupband[0]
        elif (self.st[-1] == pre_upband) and (self.data.close[0] > self.finalupband[0]):
            self.st[0] = self.finallowband[0]
            self.lines.super_trend[0] = self.finallowband[0]
        elif (self.st[-1] == pre_lowband) and (self.data.close[0] >= self.finallowband[0]):
            self.st[0] = self.finallowband[0]
            self.lines.super_trend[0] = self.finallowband[0]
        elif (self.st[-1] == pre_lowband) and (self.data.close[0] < self.finallowband[0]):
            self.st[0] = self.finalupband[0]
            self.lines.super_trend[0] = self.st[0]

class BuySellArrows(bt.observers.BuySell):
    plotlines = dict(buy=dict(marker='$\u21E7$', markersize=16.0),
                     sell=dict(marker='$\u21E9$', markersize=16.0))

class AccumulativeSwingIndex(bt.Indicator):
    lines = ('asi',)
    params = (
        ('period', 14),  # Period for the ASI calculation
    )

    def __init__(self):
        # Calculate ASI using a custom function
        self.addminperiod(self.params.period)
        self.lines.asi = bt.indicators.WMA(
        self.data.close - self.data.open,
        period=self.params.period
        ) + bt.indicators.SumN(
        self.data.high - self.data.low,
        period=self.params.period
        )


class MF_REDFLOW_STRATEGY(BaseStrategy):
    params = (
        ('stlen', 7),
        ('stmult', 7.0),
        ('stsmooth', 5),
        ('epstmult', 3.0),
        ('useep', True),
        ('tppct', False),
        ('tprsx', True),
        ('tpgap', 0.1),
        ('tpmax', 0.1),
        ('tpamt', 0.3),
        ('rlrsx', True),
        ('rlsfp', True),
        ('rsxsrc', 'hlc3'),
        ('rsxlen', 14),
        ('rsxlkb', 20),
        ('rsxob', 75),
        ('rsxos', 25),
        ('rsxignpct', 6),
        ('stop_loss_pct', 0.03),
        ('backtest', None)
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        BuySellArrows(self.data0, barplot=True)
        
        self.asi_short = AccumulativeSwingIndex(period=7)
        self.asi_long = AccumulativeSwingIndex(period=14)
        # self.asi = AccumulativeSwingIndex()
        # Track price and flip price for the position
        self.price = None
        self.flipprice = None
        self.tpprice = None
        self.prevtpprice = None
        self.tpnum = 0

        # Create a custom line for plotting TP levels
        self.lines.take_profit = bt.LineNum(1)  # Initialized with NaN (not visible until a value is set)

        # Indicators
        self.sttrend = SuperTrend(self.data, period=self.p.stlen, multiplier=self.p.stmult)
        self.eplevel = bt.ind.SMA(self.data.close, period=self.p.stsmooth)
        self.rsx = RSX(self.data, length=self.p.rsxlen)

        # Buy/Sell Signals
        self.stSfpLong = bt.ind.CrossOver(self.data.close, self.sttrend)
        self.stSfpShort = bt.ind.CrossDown(self.data.close, self.sttrend)

    def next(self):
        # Check if we are in a position
        if self.position.size == 0:
            # Check for long entry signal (SuperTrend crossover upwards)
            if self.stSfpLong:
                self.buy(size=100)
                self.price = self.data.close[0]
                self.flipprice = self.data.close[0]
                self.tpnum = 0
                self.prevtpprice = self.data.close[0]
                print(f'Entering Long at {self.data.close[0]}')

            # Check for short entry signal (SuperTrend crossover downwards)
            elif self.stSfpShort:
                self.sell(size=100)
                self.price = self.data.close[0]
                self.flipprice = self.data.close[0]
                self.tpnum = 0
                self.prevtpprice = self.data.close[0]
                print(f'Entering Short at {self.data.close[0]}')

        elif self.position.size > 0:  # Long position management
            # Update flip price if we are still in a long position
            if self.data.close[0] < self.flipprice:
                self.flipprice = self.data.close[0]

            # Stop loss for long position
            if self.data.close[0] < self.price * (1 - self.p.stop_loss_pct):
                print(f'Stop Loss hit, exiting Long at {self.data.close[0]}')
                self.close()

            # Manage take profits for long positions
            if self.tpnum < self.p.tpmax and self.data.close[0] > self.prevtpprice * (1 + self.p.tpgap / 100):
                self.tpnum += 1
                self.tpprice = self.data.close[0]
                self.prevtpprice = self.data.close[0]
                print(f'Take Profit {self.tpnum} hit at {self.data.close[0]}')

                # Set the take profit line value at the TP price for the current point
                self.lines.take_profit[0] = self.tpprice

            # Exit position if all take profits are hit or flip price is breached
            if self.tpnum >= self.p.tpmax or self.data.close[0] < self.flipprice:
                print(f'Exiting Long at {self.data.close[0]}')
                self.close()

        elif self.position.size < 0:  # Short position management
            # Update flip price if we are still in a short position
            if self.data.close[0] > self.flipprice:
                self.flipprice = self.data.close[0]

            # Stop loss for short position
            if self.data.close[0] > self.price * (1 + self.p.stop_loss_pct):
                print(f'Stop Loss hit, exiting Short at {self.data.close[0]}')
                self.close()

            # Manage take profits for short positions
            if self.tpnum < self.p.tpmax and self.data.close[0] < self.prevtpprice * (1 - self.p.tpgap / 100):
                self.tpnum += 1
                self.tpprice = self.data.close[0]
                self.prevtpprice = self.data.close[0]
                print(f'Take Profit {self.tpnum} hit at {self.data.close[0]}')

                # Set the take profit line value at the TP price for the current point
                self.lines.take_profit[0] = self.tpprice

            # Exit position if all take profits are hit or flip price is breached
            if self.tpnum >= self.p.tpmax or self.data.close[0] > self.flipprice:
                print(f'Exiting Short at {self.data.close[0]}')
                self.close()


class aLcas_STrend_AccumulativeSwingIndex(BaseStrategy):
    params = (
        ('stlen', 7),
        ('stmult', 7.0),
        ("dca_deviation", 1.5),
        ("take_profit", 2),
        ('percent_sizer', 0.1),
        ('backtest', None)
    )
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        BuySellArrows(self.data0, barplot=True)
        self.DCA = True
        
        self.asi_short = AccumulativeSwingIndex(period=7, plot=False)
        self.asi_long = AccumulativeSwingIndex(period=14, plot=False)
        # Indicators
        self.sttrend = SuperTrend(self.data, period=self.p.stlen, multiplier=self.p.stmult, plot=False)

        # Buy/Sell Signals
        self.stLong = bt.ind.CrossOver(self.data.close, self.sttrend, plot=False)
        self.stShort = bt.ind.CrossDown(self.data.close, self.sttrend, plot=False)

    def buy_or_short_condition(self):
        if not self.buy_executed and not self.conditions_checked:
            if self.stLong and self.asi_short[0] > self.asi_short[-1] and self.asi_short[0] > 5 and self.asi_long[0] > self.asi_long[-1]:

                if self.params.backtest == False:
                    self.entry_prices.append(self.data.close[0])
                    print(f'\n\n\nBUY EXECUTED AT {self.data.close[0]}\n\n\n')
                    self.sizes.append(self.amount)
                    # self.load_trade_data()
                    self.enqueue_order('buy', exchange=self.exchange, account=self.account, asset=self.asset, amount=self.amount)
                    self.calc_averages()
                    self.buy_executed = True
                    self.conditions_checked = True
                elif self.params.backtest == True:
                    self.buy(size=self.stake, price=self.data.close[0], exectype=bt.Order.Market)
                    self.buy_executed = True
                    self.entry_prices.append(self.data.close[0])
                    self.sizes.append(self.stake)
                    self.calc_averages()
                    self.conditions_checked = True

    def dca_or_short_condition(self):
        if self.buy_executed and not self.conditions_checked:
            if self.stLong and self.asi_short[0] > self.asi_short[-1] and self.asi_short[0] > 5 and self.asi_long[0] > self.asi_long[-1]:

                if self.entry_prices and self.data.close[0] < self.entry_prices[-1] * (1 - self.params.dca_deviation / 100):    
                    if self.params.backtest == False:
                        self.entry_prices.append(self.data.close[0])
                        self.sizes.append(self.amount)
                        # self.load_trade_data()
                        print(f'\n\n\nBUY EXECUTED AT {self.data.close[0]}\n\n\n')
                        self.enqueue_order('buy', exchange=self.exchange, account=self.account, asset=self.asset, amount=self.amount)
                        self.calc_averages()
                        self.buy_executed = True
                        self.conditions_checked = True
                    elif self.params.backtest == True:
                        self.buy(size=self.stake, price=self.data.close[0], exectype=bt.Order.Market)
                        self.buy_executed = True
                        self.entry_prices.append(self.data.close[0])
                        self.sizes.append(self.stake)
                        self.calc_averages()
                        self.conditions_checked = True

    def sell_or_cover_condition(self):
        if self.buy_executed and self.data.close[0] >= self.take_profit_price:
            average_entry_price = sum(self.entry_prices) / len(self.entry_prices) if self.entry_prices else 0

            # Avoid selling at a loss or below the take profit price
            if round(self.data.close[0], 9) < round(self.average_entry_price, 9) or round(self.data.close[0], 9) < round(self.take_profit_price, 9):
                print(
                    f"| - Avoiding sell at a loss or below take profit. "
                    f"| - Current close price: {self.data.close[0]:.12f}, "
                    f"| - Average entry price: {average_entry_price:.12f}, "
                    f"| - Take profit price: {self.take_profit_price:.12f}"
                )
                self.conditions_checked = True
                return

            if self.params.backtest == False:
                self.enqueue_order('sell', exchange=self.exchange, account=self.account, asset=self.asset)
            elif self.params.backtest == True:
                self.close()

            self.reset_position_state()
            self.buy_executed = False
            self.conditions_checked = True

from fastquant import get_database_stock_data, backtest
crypto = get_database_stock_data("EUR_USD", "2013-01-01", "2023-10-04", "1m")
backtest(MF_REDFLOW_STRATEGY, 
        crypto,
        init_cash=1000,
        backtest=True)