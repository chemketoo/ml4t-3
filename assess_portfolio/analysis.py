"""Analyze a portfolio.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):


    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

       # initial allocations
    #weight = 1.0/len(syms)
    #allocs = np.zeros(len(syms))
    #allocs[0:].fill(weight)

    # normalize prices
    normalized_prices = prices / prices.values[0]

    total_allocations = normalized_prices * allocs
    position_val = total_allocations * sv
    portfolio_val = position_val.sum(axis=1)
    
    daily_returns = prices.copy()
    daily_returns = portfolio_val/portfolio_val.shift(1) - 1
    daily_returns.iloc[0] = 0
    

    #allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations 			  		 			 	 	 		 		 	  		   	  			  	
    # cumulative return, avg daily return, stDev daily return, sharpe ratio
    #cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats 			  		 			 	 	 		 		 	  		   	  			  	
    cr = (portfolio_val[-1] / portfolio_val[0]) - 1
    adr = daily_returns[1:].mean() 		
    sddr = daily_returns[1:].std()
    sr =  np.sqrt(sf) * (daily_returns[1:] - rfr).mean() / sddr  		 			 	 	 		 		 	  		   	  			  	

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([portfolio_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        pass

    # Add code here to properly compute end value
    ev = portfolio_val[-1]

    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2010,1,1)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    test_code()
