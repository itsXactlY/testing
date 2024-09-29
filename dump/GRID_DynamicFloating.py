import backtrader as bt
import numpy as np


class BuySellArrows(bt.observers.BuySell):
    plotlines = dict(buy=dict(marker='$\u21E7$', markersize=12.0),
                     sell=dict(marker='$\u21E9$', markersize=12.0))

class DynamicGridStrategy(bt.Strategy):
    params = (
        ('period', 1440),    # Moving window period for highest and lowest indicators
        ('num_levels', 20),         # Number of levels above and below the midpoint
        ('grid_interval', 0.001),  # Interval between grid levels (0.5%) -> 0.005 is 5%
        ('backtest', None),
    )

    def __init__(self):
        super().__init__()
        BuySellArrows(self.data0, barplot=True)
        # Calculate the highest high and lowest low over the specified moving window period
        self.highest = bt.indicators.Highest(self.data.high, period=self.params.period, subplot=False)
        self.lowest = bt.indicators.Lowest(self.data.low, period=self.params.period, subplot=False)
        self.mid = (self.highest + self.lowest) / 2
        # Initialize the price levels
        self.last_price_index = None

    def calculate_price_levels(self):
        perc_levels = [1 + self.params.grid_interval * i for i in range(self.params.num_levels, -self.params.num_levels - 1, -1)]
        self.price_levels = [self.mid[0] * x for x in perc_levels]


    def update_grid(self):
        # Ensure there is enough data before calculating grid levels
        if len(self.data) < self.params.period:
            return
        
        # Calculate the midpoint between the highest high and the lowest low
        mid = (self.highest[0] + self.lowest[0]) / 2
        # Define percentage levels for the grid, creating levels at specified intervals above and below the midpoint
        perc_levels = [x for x in np.arange(1 + self.params.grid_interval * 5, 1 - self.params.grid_interval * 5 - self.params.grid_interval / 2, -self.params.grid_interval)]
        # Calculate the actual price levels for the grid based on the midpoint and the percentage levels
        self.price_levels = [mid * x for x in perc_levels]
        # Log the updated grid levels for debugging
        # self.log(f'Updated grid levels: {self.price_levels}')

    def next(self):
        # Check if there is enough data to calculate the highest and lowest indicators
        if len(self.data) < self.params.period:
            return

        # Check if there are no open positions
        if self.position.size == 0:
            self.calculate_price_levels()
            self.last_price_index = None

        # Update the grid dynamically based on the latest highest and lowest prices
        self.update_grid()

        # Ensure there is enough data and grid levels have been initialized
        if len(self.data) < self.params.period or not hasattr(self, 'price_levels'):
            return

        # On the first run, determine the initial position based on the current close price
        if self.last_price_index is None:
            for i in range(len(self.price_levels)):
                if self.data.close[0] > self.price_levels[i]:
                    # Set the last price index to the current index if the close price is above the current level
                    self.last_price_index = i
                    # Set the target portfolio percentage to be proportional to the index position in the grid
                    self.order_target_percent(target=i / (len(self.price_levels) - 1))
                    return
        else:
            # If not the first run, check for signals to adjust the position
            signal = False
            while True:
                upper = None
                lower = None

                # Determine the upper and lower price levels adjacent to the current price level
                if self.last_price_index > 0:
                    upper = self.price_levels[self.last_price_index - 1]
                if self.last_price_index < len(self.price_levels) - 1:
                    lower = self.price_levels[self.last_price_index + 1]

                # If the close price is above the upper level and we are not at the lightest position, sell more
                if upper is not None and self.data.close[0] > upper:
                    self.last_price_index -= 1
                    signal = True
                    continue

                # If the close price is below the lower level and we are not at the heaviest position, buy more
                if lower is not None and self.data.close[0] < lower:
                    self.last_price_index += 1
                    signal = True
                    continue
                break

            # If a signal was generated, adjust the target portfolio percentage accordingly
            if signal:
                self.order_target_percent(target=self.last_price_index / (len(self.price_levels) - 1))

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')
