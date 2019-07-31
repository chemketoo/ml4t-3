""" 			  		 			 	 	 		 		 	  		   	  			  	
Template for implementing StrategyLearner  (c) 2016 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			 	 	 		 		 	  		   	  			  	
Atlanta, Georgia 30332 			  		 			 	 	 		 		 	  		   	  			  	
All Rights Reserved 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Template code for CS 4646/7646 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			 	 	 		 		 	  		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			 	 	 		 		 	  		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			 	 	 		 		 	  		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			 	 	 		 		 	  		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			 	 	 		 		 	  		   	  			  	
or edited. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			 	 	 		 		 	  		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			 	 	 		 		 	  		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			 	 	 		 		 	  		   	  			  	
GT honor code violation. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
-----do not edit anything above this line--- 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
""" 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  	
import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import util as ut 			  		 			 	 	 		 		 	  		   	  			  	
import random 		
import QLearner as ql	 
import indicators as ind
from marketsimcode import compute_portvals 	 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
class StrategyLearner(object): 	
    # position constants
    _long = 1
    _short = -1
    _cash = 0 # aka do nothing		  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # constructor 			  		 			 	 	 		 		 	  		   	  			  	
    def __init__(self, verbose = False, impact=0.0, **kwargs): 			  		 			 	 	 		 		 	  		   	  			  	
        self.verbose = verbose 			  		 			 	 	 		 		 	  		   	  			  	
        self.impact = impact 	
        self.bbp_bins = None
        self.sma_bins = None
        self.momentum_bins = None
        self.nbins = 9
        self.learner = ql.QLearner(**kwargs)

    def getState(self, bbp, sma, momentum, dates):
        out_bbp, bins_bbp = pd.qcut(bbp.iloc[:, 0], self.nbins, labels=False, precision=0, retbins=True)
        out_sma, bins_sma = pd.qcut(sma.iloc[:, 0], self.nbins, labels=False, precision=0, retbins=True)
        out_momentum, bins_momentum = pd.qcut(momentum.iloc[:, 0], self.nbins, labels= False, precision=0, retbins=True)
        self.bbp_bins = out_bbp
        self.sma_bins = out_sma
        self.momentum_bins = out_momentum

        # from Piazza, binary decimal conversion
        xstate = (out_bbp * self.nbins**2) + (out_sma * self.nbins**1) + (out_momentum * self.nbins**0)
        # drop any nans. They're from the extra look ahead for the first trading day
        # drop anything not in our range
        xstate = xstate.dropna()
        xstate = xstate[xstate.index.isin(dates)].astype(int)  
        return xstate

    def getPosition(self, curr_pos, trade_signal):
        
        # if currently long or hold (1, 0), go short
        if curr_pos > self._short and trade_signal == self._short:
            next_pos = self._short
        # if currently hold or short (-1, 0), go long
        elif curr_pos < self._long and trade_signal == self._long:
            next_pos = self._long
        else:
            next_pos = self._cash
        return next_pos

    def getIndicators(self, dates, ed, syms, window=14, lookback=3):
        # I can look back at historical data before
        # the actual start date of the portfolio as
        # long as I only use that for technical analysis
        lookback_dates = pd.date_range(dates[0] - (window * 2), ed)
        prices_w_lookback = ut.get_data(syms, lookback_dates, addSPY=True, colname='Adj Close')[syms]

        bbp = ind.bollinger_percentage(prices_w_lookback, window)
        sma = ind.sma(prices_w_lookback, window)
        momentum = ind.momentum(prices_w_lookback, lookback)

        return bbp, sma, momentum

    
    def updateTrades(self, curr_pos, position, numShares, action, day, trades_df):
        '''
        mappings
        position (action - 1): -1 (short), 0 (cash), 1 (long)
        action : 0 (short), 1 (hold/nop), 2 (long)
        '''
        if action == 0: # short/sell
            if numShares > -1000:
                if numShares == 0:
                    trades_df.loc[day] = -1000
                    numShares = numShares - 1000
                else:
                    trades_df.loc[day] = -2000
                    numShares = numShares - 2000
            '''
            #keep
            if numShares != -1000:
                trades_df.loc[day] = -1000 - numShares
                numShares = -1000
            '''

        if action == 2: # long/buy
            if numShares < 1000:
                if numShares == 0:
                    trades_df.loc[day] = 1000
                    numShares += 1000
                else:
                    trades_df.loc[day] = 2000
                    numShares += 2000
            '''
            ## keep
            if numShares != 1000:
                trades_df.loc[day] = 1000 - numShares
                numShares = 1000
            '''


        '''
        if curr_pos == self._long: # own shares
            if action == 0: # short
                if numShares > -1000:
                    trades_df.loc[day] = -1000 - numShares
                    numShares = -1000
            if action == 2: # long
                if numShares < 1000:
                    trades_df.loc[day] = 1000 - numShares
                    numShares = 1000
        elif curr_pos == self._short: # short shares
            if action == 0: # short
                if numShares > -1000:
                    trades_df.loc[day] = -1000 - numShares
                    numShares = -1000
            if action == 2: #
                if numShares < 1000:
                    trades_df.loc[day] = 1000 - numShares
                    numShares = 1000
        elif curr_pos == self._cash: # nothing
            if numShares == 0:
                if action == 2: #long
                    trades_df.loc[day] = 1000 - numShares
                    numShares = 1000
                if action == 0: # sell/short
                    trades_df.loc[day] = -1000 - numShares
                    numShares = -1000
        '''
        position = curr_pos
        return trades_df, numShares, position

    def isConverged(self, accum_returns, set_size=20):
        set_rets = accum_returns[-set_size:] # checking most recent
        max_ret = max(accum_returns)
        # all same returns
        if len(pd.unique(set_rets)) == 1:
            return True
        if max_ret in set_rets: # is in the most recent set
            if max_ret not in accum_returns[:len(accum_returns) - set_size]:
                return False
            else:
                return True
        return True
        
 			  		 			 	 	 		 		 	  		   	  			  	
    # this method should create a QLearner, and train it for trading 			  		 			 	 	 		 		 	  		   	  			  	
    def addEvidence(self, symbol = "JPM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000): 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        # states - num steps ** num indicators
        # actions - buy, sell, do nothing
        syms = []
        syms.append(symbol)
        dates = pd.date_range(sd, ed)

        prices_sym = ut.get_data(syms, dates, addSPY=False, colname='Adj Close')
        prices_sym = prices_sym.dropna()

        bbp, sma, momentum = self.getIndicators(dates, ed, syms)

        self.learner = ql.QLearner(num_states=self.nbins**3,\
        num_actions = 3, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.999, \
        dyna = 0, \
        verbose=False)
       
        converged = False
        # all states
        xstate = self.getState(bbp, sma, momentum, dates)
        reward = 0
        # maximum number of runs for learner
        max_runs = 100

        # learner trades
        l_trade_df = prices_sym.copy()
        
        all_cum_returns = []
        minRuns = 15
        for run in range(0, max_runs):
            position = self._cash
            l_trade_df.iloc[:,:] = 0
            l_trade_df.iloc[:,-1] = 0.0
            numShares = 0
        
            for day, row in prices_sym.iterrows():
                x = xstate.at[day]
                
                # if first day
                if prices_sym.iloc[0, 0] == prices_sym.at[day, symbol]:
                    action = self.learner.querysetstate(x)
                else:
                    day_index = prices_sym.index.get_loc(day)
                    dr = (prices_sym.at[day, symbol] / prices_sym.iloc[day_index - 1])
                    reward = position * action * dr         
                    action = self.learner.query(x, reward)
               
                # action is 0, 1, 2, subtract 1 from action
                # to get -1, 0, 1 to short, hold, or go long
                # for trade signal
                curr_pos = self.getPosition(position, action - 1)
                
                # update trades
                l_trade_df, numShares, position = self.updateTrades(curr_pos, position, numShares, action, day, l_trade_df)
           
            strat_port_vals = compute_portvals(l_trade_df, start_val=sv, commission=0.0, impact=self.impact)
            cum_return = strat_port_vals.iloc[-1, 0] / strat_port_vals.iloc[0, 0] - 1.0
            
            all_cum_returns.append(cum_return)
            # build up some runs before checking convergence
            if run > minRuns:
                if self.isConverged(all_cum_returns, minRuns):
                    break  		 			 	 	 		 		 	  		   	  			  	 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # this method should use the existing policy and test it against new data 			  		 			 	 	 		 		 	  		   	  			  	
    def testPolicy(self, symbol = "JPM", \
        sd=dt.datetime(2010,1,1), \
        ed=dt.datetime(2011,12,31), \
        sv = 100000): 			  		 			 	 	 		 		 	  		   	  			  	
        self.learner.rar = 0.0 # no randomness in test
        syms = []
        syms.append(symbol)
        dates = pd.date_range(sd, ed)
     
        prices_sym = ut.get_data(syms, dates, addSPY=False, colname='Adj Close')
        prices_sym = prices_sym.dropna()
        
        trades = prices_sym.copy()
        trades[:] = 0

        bbp, sma, momentum = self.getIndicators(dates, ed, syms)

        # all states
        xstate = self.getState(bbp, sma, momentum, dates)

        position = self._cash

        numShares = 0
        for day, row in prices_sym.iterrows():
                x = xstate.at[day]
                
                action = self.learner.querysetstate(x)
                curr_pos = self.getPosition(position, action - 1)
                # update trades
                trades, numShares, position = self.updateTrades(curr_pos, position, numShares, action, day, trades)
        return trades 			

    def author(self): 
        return 'gtusername'  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "One does not simply think up a strategy"
    sl = StrategyLearner() 	
    sl.addEvidence()
    sl.testPolicy()		  		 			 	 	 		 		 	  		   	  			  	
