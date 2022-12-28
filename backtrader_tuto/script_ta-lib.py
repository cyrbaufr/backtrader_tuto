from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt

# Template of the file can be found here:
# https://www.programmersought.com/article/38017224688/
# See also https://www.programmersought.com/article/10344701952/


# Create a Strategy
class TestStrategy(bt.Strategy):
    params = (
        ('RSI6period', 6),
        ('RSI24period', 24),
    )

    def log(self, txt, dt=None):
        """ Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        # Add Ta-Lib RSI indicator
        self.RSI6 = bt.talib.RSI(self.data, timeperiod=self.p.RSI6period)
        self.RSI24 = bt.talib.RSI(self.data, timeperiod=self.p.RSI24period)
        self.crossover = bt.ind.CrossOver(self.RSI6, self.RSI24)  # Cross signal

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        if not self.position:
            if self.crossover > 0:
                self.order = self.buy()
            elif self.RSI6[0] < 30:
                self.order = self.buy()
        else:
            if self.crossover < 0:
                self.order = self.close()
            elif self.RSI6[0] > 80:
                self.order = self.buy()

            # Create a cerebro entity


# Execute Backtest

# To execute, run python3 script_ta-lib.py in a terminal
# In case of error 'No module named 'tkinter'
# sudo apt-get install python3.x-tk
# with python3.x python version used in venv

cerebro = bt.Cerebro()
# Add a strategy
cerebro.addstrategy(TestStrategy)
# Create a Data Feed
# load a Dataset from a csv file
data = bt.feeds.YahooFinanceCSVData(
        # select file
        dataname='data/orcl-1995-2014.csv',
        # select start date
        fromdate=datetime.datetime(2000, 1, 1),
        # select end date
        todate=datetime.datetime(2000, 12, 31),
        # put dates in ascending order
        reverse=False)
# Add the Data Feed to Cerebro
cerebro.adddata(data)
# Set our desired cash start
cerebro.broker.setcash(100000.0)
# Set the size of the trading unit 100 shares of A shares as one lot
cerebro.addsizer(bt.sizers.FixedSize, stake=100)

# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
# Run over everything
cerebro.run()
# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
# Plot the result
cerebro.plot()
