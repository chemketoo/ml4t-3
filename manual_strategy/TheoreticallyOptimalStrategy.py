import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 	
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data 	
from marketsimcode import compute_portvals

class TheoreticallyOptimalStrategy(object):

    def __init__(self, commission=0.0, impact=0.0):
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
        #print(init_trade)
        benchmark_portfolio = compute_portvals(init_trade, start_val=100000, commission=self.commission, impact=self.impact)

        # optimal
        opt_trade = init_trade.copy()
        opt_trade.iloc[:,:] = 0
        opt_trade.iloc[:,-1] = 0.0

        position = 0
        for i in range(prices_sym.shape[0] - 1):
            if prices_sym.iloc[i][symbol] < prices_sym.iloc[i + 1][symbol]:
                opt_trade.iloc[i][symbol] = 1000 - position
                position = 1000
            else:
                opt_trade.iloc[i][symbol] = -1000 - position
                position = -1000
        optimal_portfolio = compute_portvals(opt_trade, start_val=100000, commission=self.commission, impact=self.impact)

        fig = plt.figure()
        plt.title('Theoretically Optimal Strategy')
        x = benchmark_portfolio.index.values # dates
        y = benchmark_portfolio.values
        y = y/y[0] # normalize?
        plt.plot(x, y, color='green', label='Benchmark')
        x2 = optimal_portfolio.index.values
        y2 = optimal_portfolio.values
        y2 = y2/y2[0]
        plt.plot(x2, y2, color='red', label='Theoretically Optimal Strategy')
        plt.tight_layout()
        plt.legend()
        plt.savefig('TOS_' + str(sd.year) + '.png')

        # stats
        daily_returns_bench = benchmark_portfolio / benchmark_portfolio.shift(1) - 1
        c_return_bench = benchmark_portfolio.iloc[-1] / benchmark_portfolio.iloc[0] - 1
        stdev_daily_bench = daily_returns_bench.std()
        mean_daily_bench = daily_returns_bench.mean()
        
        daily_returns_opt = optimal_portfolio / optimal_portfolio.shift(1) - 1
        c_return_opt = optimal_portfolio.iloc[-1] / optimal_portfolio.iloc[0] - 1
        stdev_daily_opt = daily_returns_opt.std()
        mean_daily_opt = daily_returns_opt.mean()

        print('Benchmark Stats')
        print('Cumulative Return: ' + str(c_return_bench))
        print('StDev Daily: ' + str(stdev_daily_bench))
        print('Mean Daily: ' + str(mean_daily_bench))

        print('Optimal Stats')
        print('Cumulative Return: ' + str(c_return_opt))
        print('StDev Daily: ' + str(stdev_daily_opt))
        print('Mean Daily: ' + str(mean_daily_opt))
    
    def author():
        return 'gtusername'

if __name__ == "__main__":
    tos = TheoreticallyOptimalStrategy()
    # default in sample test case
    tos.testPolicy()
    # out sample test case
    #tos.testPolicy(symbol="JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31))