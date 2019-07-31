'''

'''			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  	
import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import util as ut 			  		 			 	 	 		 		 	  		   	  			  	
import random 		
import QLearner as ql	 
import ManualStrategy as ms
import StrategyLearner as sl
import indicators as ind
from marketsimcode import compute_portvals 	 	
import matplotlib.pyplot as plt

def author(self): 
    return 'gtusername'  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 
    sym = "JPM"
    sv = 100000
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    slearner = sl.StrategyLearner(verbose=False, impact=0.0)
    slearner.addEvidence(symbol=sym, sd=sd, ed=ed, sv=sv)
    trades_sl = slearner.testPolicy(symbol=sym, sd=sd, ed=ed, sv=100000)

    # strat learner portfolio
    portvals_sl = compute_portvals(trades_sl, sv)

    # man strategy
    mslearner = ms.ManualStrategy(impact=0.0)
    trades_ms = mslearner.testPolicy(symbol=sym, sd=sd, ed=ed, sv=sv)
    portvals_ms = compute_portvals(trades_ms, sv)

    # compare
    dates = pd.date_range(sd, ed)
    syms = ['SPY']
    prices_SPY = ut.get_data(syms, dates, addSPY=True, colname='Adj Close')
    prices_SPY = prices_SPY[syms]

    prices_norm = prices_SPY / prices_SPY.values[0]
    prices_norm = prices_norm.dropna(how='all')
    prices_norm = prices_norm.fillna(method='ffill')
    prices_norm = prices_norm.fillna(method='bfill')
    port_sl_norm = portvals_sl / portvals_sl.values[0]
    port_ms_norm = portvals_ms / portvals_ms.values[0]

    all_vals = pd.concat([port_ms_norm, port_sl_norm, prices_norm], axis=1)
    all_vals.columns = ['Manual Strategy', 'Strategy Learner', 'SPY']

    all_vals.plot(title='Manual vs Strategy Learner', use_index=True, )
    plt.legend()
    plt.grid()
    plt.savefig('experiment1.png')