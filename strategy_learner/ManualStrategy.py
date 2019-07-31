import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 	
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from util import get_data 	
from marketsimcode import compute_portvals
import indicators as ind

class ManualStrategy(object):
    def __init__(self, commission=9.95, impact=0.005):
        self.commission = commission
        self.impact = impact

    def testPolicy(self, symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000):
        dates = pd.date_range(sd, ed)
        syms = []
        syms.append(symbol)
        prices_SPY = get_data(syms, dates, addSPY=True, colname='Adj Close')
        prices_sym = prices_SPY[syms]
        init_trade = prices_sym.copy()
        init_trade[:] = 0

        # benchmark - buy and hold 1000 shares
        init_trade.iloc[0,0] = 1000
        benchmark_portfolio = compute_portvals(init_trade, start_val=100000, commission=0.0, impact=0.0)

        # manual strategy
        man_trade = prices_sym.copy()
        man_trade[:] = 0
        window = 14
        lookback = 3
        # I can look back at historical data before
        # the actual start date of the portfolio as
        # long as I only use that for technical analysis
        lookback_dates = pd.date_range(dates[0] - (window * 2), ed)
        prices_w_lookback = get_data(syms, lookback_dates, addSPY=True, colname='Adj Close')[syms]

        bbp = ind.bollinger_percentage(prices_w_lookback, window)
        sma = ind.sma(prices_w_lookback, window)
        momentum = ind.momentum(prices_w_lookback, lookback)
        # One DF for iterating
        indicators = pd.concat([bbp, sma, momentum], axis=1)
        indicators.columns = ['BBP', 'SMA', 'Momentum']
        indicators = indicators.dropna() # Just drop any day where we have NAN

        man_trade = init_trade.copy()
        man_trade.iloc[:,:] = 0
        man_trade.iloc[:,-1] = 0.0
        # track long and short positions
        longPos = []
        shortPos = []

        position = 0
        for i in range(indicators.shape[0] - 1):
            # dropna removes some dates from indicators, can't rely on index
            date = indicators.iloc[i].name.strftime('%Y-%m-%d')
            if (indicators.iloc[i]['BBP'] < .03) and (indicators.iloc[i]['Momentum'] > -0.2) and (indicators.iloc[i]['SMA'] < .97):
                #BUY
                if position != 1000:
                    man_trade.loc[date][syms] = 1000 - position
                    position = 1000
                    longPos.append(date)
            elif (indicators.iloc[i]['BBP'] > .97) and (indicators.iloc[i]['Momentum'] < 0.2) and (indicators.iloc[i]['SMA'] > 1.03):
                #SELL
                if position != -1000:
                    man_trade.loc[date][syms] = -1000 - position
                    position = -1000
                    shortPos.append(date)
        '''
        man_portfolio = compute_portvals(man_trade, start_val=100000, commission=self.commission, impact=self.impact)

        # Strategy vs Benchmark
        fig = plt.figure()
        plt.title('Manual Strategy')
        x = benchmark_portfolio.index.values # dates
        y = benchmark_portfolio.values
        y = y/y[0] # normalize
        plt.plot(x, y, color='green', label='Benchmark')
        x2 = man_portfolio.index.values
        y2 = man_portfolio.values
        y2 = y2/y2[0]
        plt.plot(x2, y2, color='red', label='Manual Strategy')

        plt.tight_layout()
        plt.legend()
        plt.savefig('MS_' + str(sd.year) + '.png')

        # Entry points
        plt.clf()
        fig = plt.figure
        plt.title('Entry Points')
        x = prices_sym.index.values
        y = prices_sym.values / prices_sym.values[0]
        plt.plot(x, y, color='orange', label='Prices')
        # plot longs
        for l in longPos:
            y = prices_sym.loc[l][0] / prices_sym.iloc[0,0]
            plt.plot([l, l], [y + .1, y -.1], color='blue')
        for s in shortPos:
            y = prices_sym.loc[s][0] / prices_sym.iloc[0,0]
            plt.plot([s, s], [y + .1, y - .1], color='black')

        plt.grid()
        # custom legend entries for long and short
        ax = plt.gca()
        handles, labels = ax.get_legend_handles_labels()
        long_line = mlines.Line2D([],[], color='blue', label='Long')
        short_line = mlines.Line2D([],[], color='black', label='Short')
        handles.append(long_line)
        handles.append(short_line)
        plt.legend(handles=handles)
        plt.tight_layout()
        plt.savefig('entrypoints_MS_' + str(sd.year) + '.png')

        # Stats
        daily_returns_bench = benchmark_portfolio / benchmark_portfolio.shift(1) - 1
        c_return_bench = benchmark_portfolio.iloc[-1] / benchmark_portfolio.iloc[0] - 1
        stdev_daily_bench = daily_returns_bench.std()
        mean_daily_bench = daily_returns_bench.mean()
        
        daily_returns_opt = man_portfolio / man_portfolio.shift(1) - 1
        c_return_opt = man_portfolio.iloc[-1] / man_portfolio.iloc[0] - 1
        stdev_daily_opt = daily_returns_opt.std()
        mean_daily_opt = daily_returns_opt.mean()

        print('Benchmark Stats')
        print('Cumulative Return: ' + str(c_return_bench))
        print('StDev Daily: ' + str(stdev_daily_bench))
        print('Mean Daily: ' + str(mean_daily_bench))

        print('Manual Stats')
        print('Cumulative Return: ' + str(c_return_opt))
        print('StDev Daily: ' + str(stdev_daily_opt))
        print('Mean Daily: ' + str(mean_daily_opt))
        '''
        return man_trade

def author():
    return 'gtusername'

if __name__ == "__main__":
    ms = ManualStrategy()
    # default in sample test
    ms.testPolicy()
    # out sample test case
    #ms.testPolicy(symbol="JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31))