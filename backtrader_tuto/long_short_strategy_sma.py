from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
# import statsmodel as sm
# Import the backtrader platform
import backtrader as bt

# Source of the file:
# https://www.programmersought.com/article/21454686228/
# This file has not been tested yet & does not work!


# Create a Strategy
class TestStrategy(bt.Strategy):
    params = (
        # Standard MACD Parameters
        ('period', 252),
        ('prepend_constant', True),
    )

    def log(self, txt, dt=None):
        """ Logging function for this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose_x = self.datas[0].close
        self.dataclose_y = self.datas[1].close
        self.ma1 = bt.indicators.MovingAverageSimple(self.datas[0],
                                     period=self.p.period
                                     )
        self.ma2 = bt.indicators.SMA(self.datas[1],
                                       period=self.p.period
                                      )
        self.order = None
        self.buyprice = None
        self.buycomm = None

    def notify_cashvalue(self, cash, value):
        self.log('Cash %s Value %s' % (cash, value))
    def notify_order(self, order):
        print(type(order), 'Is Buy ', order.isbuy())
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
        self.log('Close, %.2f' % self.dataclose_x[0])
        self.log('Close, %.2f' % self.dataclose_y[0])
        # Check if we are in the market
        if not self.getposition(self.datas[1]):


            # Not yet ... we MIGHT BUY if ...
            if (self.ma1[0]-self.ma1[-1])/self.ma1[-1]>(self.ma2[0]-self.ma2[-1])/self.ma2[-1]:
                    #if sma[0]<top[-5]:
                        # BUY, BUY, BUY!!! (with default parameters)
                        self.log('BUY CREATE,{},{}'.format(self.dataclose_y[0],self.dataclose_x[0]) )


                        # Keep track of the created order to avoid a 2nd order
                        self.order=self.buy(self.datas[0])
                        self.order = self.sell(self.datas[1])



        else:

            # Already in the market ... we might sell
            if (self.ma1[0]-self.ma1[-1])/self.ma1[-1]<=(self.ma2[0]-self.ma2[-1])/self.ma2[-1]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('BUY CREATE,{},{}'.format(self.dataclose_y[0],self.dataclose_x[0]) )


                # Keep track of the created order to avoid a 2nd order
                self.log('Pos size %s' % self.position.size)
                self.order = self.close(self.datas[1])
                self.order = self.close(self.datas[0])




if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    datapath_1='C:/Users/Administrator/Documents/000001.SZ.csv'
    datapath_2='C:/Users/Administrator/Documents/000002.SZ.csv'
    # Create a Data Feed
    data_1 = bt.feeds.GenericCSVData(
        dataname=datapath_1,
        # Do not pass values before this date
        fromdate=datetime.datetime(1991, 12, 23),
        # Do not pass values after this date
        todate=datetime.datetime(2017, 12, 31),
        dtformat=('%Y-%m-%d'),
        tmformat=('%H.%M.%S'),
        date=0,
        open=1,
        close=2,
        high=3,
        low=4,
        volume=5,
        openinterest=6,
        code=-1,
        reverse=False)
    data_2 = bt.feeds.GenericCSVData(
        dataname=datapath_2,
        # Do not pass values before this date
        fromdate=datetime.datetime(1991, 12, 23),
        # Do not pass values after this date
        todate=datetime.datetime(2017, 12, 31),
        dtformat=('%Y-%m-%d'),
        tmformat=('%H.%M.%S'),
        date=0,
        open=1,
        close=2,
        high=3,
        low=4,
        volume=5,
        openinterest=6,
        reverse=False)


    # Add the Data Feed to Cerebro
    cerebro.adddata(data_1)
    cerebro.adddata(data_2)


    # Set our desired cash start
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())


    # Run over everything
    cerebro.run()


    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()