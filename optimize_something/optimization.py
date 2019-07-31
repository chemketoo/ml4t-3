"""MC1-P2: Optimize a portfolio. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import matplotlib.pyplot as plt 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  	
from util import get_data, plot_data 	
import scipy.optimize as sco		  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
# This is the function that will be tested by the autograder 			  		 			 	 	 		 		 	  		   	  			  	
# The student must update this code to properly implement the functionality 			  		 			 	 	 		 		 	  		   	  			  	
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False): 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Read in adjusted closing prices for given symbols, date range 			  		 			 	 	 		 		 	  		   	  			  	
    dates = pd.date_range(sd, ed) 			  		 			 	 	 		 		 	  		   	  			  	
    prices_all = get_data(syms, dates)  # automatically adds SPY 			  		 			 	 	 		 		 	  		   	  			  	
    prices_all.fillna(method='ffill', inplace=True)
    prices_all.fillna(method='bfill', inplace=True)
    prices = prices_all[syms]  # only portfolio symbols 			  		 			 	 	 		 		 	  		   	  			  	
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # find the allocations for the optimal portfolio 			  		 			 	 	 		 		 	  		   	  			  	

    # initial allocations
    numSyms = len(syms)
    weight = 1.0/numSyms
    allocs = np.zeros(numSyms)
    allocs.fill(weight)

    # optimize allocations
    constrain = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = tuple((0,1) for x in range(numSyms))
    #rets
    rets = np.log(prices/prices.shift(1))
    # params: minimization function, initial guess (x0), args for min function, min algorithm, options-verbose
    opts = sco.minimize(minimize_func_sharpe, allocs, args=(rets), method='SLSQP', bounds=bound, constraints=constrain)
    allocs = opts.x.round(3)

    #stats
    normalized_prices = prices / prices.values[0]
    total_allocations = normalized_prices * allocs
    position_val = total_allocations * 1  # not sure if this s/b 10000 or 1
    portfolio_val = position_val.sum(axis=1)
    
    daily_returns = np.zeros(prices.shape)
    daily_returns = portfolio_val / portfolio_val.shift(1) - 1
    daily_returns.iloc[0] = 0
     			  		 			 	 	 		 		 	  		   	  			  	
    # cumulative return, avg daily return, stDev daily return, sharpe ratio			 	 	 		 		 	  		   	  			  	
    cr = (portfolio_val[-1] / portfolio_val[0]) - 1
    adr = daily_returns[1:].mean() 		
    sddr = daily_returns[1:].std()
    sr =  np.sqrt(252) * (daily_returns[1:] - 0.0).mean() / sddr  		 			 	 	 		 		 	  		   	  			  	
		  		 			 	 	 		 		 	  		   	  			  	
    # Compare daily portfolio value with SPY using a normalized plot 			  		 			 	 	 		 		 	  		   	  			  	
    #gen_plot = True
    if gen_plot: 	
        spy_data = prices_SPY / prices_SPY.values[0]		  		 			 	 	 		 		 	  		   	  			  				  		 			 	 	 		 		 	  		   	  			  	
        df_temp = pd.concat([portfolio_val, spy_data], keys=['Portfolio', 'SPY'], axis=1) 			  		 			 	 	 		 		 	  		   	  			  	

        ax = df_temp.plot(title='Daily Portfolio Value and SPY', fontsize=12)  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_xlabel('Date')  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel('Price')
        fig = ax.get_figure()
        fig.savefig('./plot.png')
        fig.clf()
        plt.close()
 			  		 			 	 	 		 		 	  		   	  			  	
    return allocs, cr, adr, sddr, sr 	

def minimize_func_sharpe(weights, rets):
    # Took this from text book, p 328, modified slightly
    weights = np.array(weights)
    expected_port_returns = np.sum(rets.mean() * weights) * 252
    expected_port_volatility = np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))
    #rf = 0
    return -(expected_port_returns / expected_port_volatility)
    
 			  		 			 	 	 		 		 	  		   	  			  	
def test_code(): 			  		 			 	 	 		 		 	  		   	  			  	
    # This function WILL NOT be called by the auto grader 			  		 			 	 	 		 		 	  		   	  			  	
    # Do not assume that any variables defined here are available to your function/code 			  		 			 	 	 		 		 	  		   	  			  	
    # It is only here to help you set up and test your code 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Define input parameters 			  		 			 	 	 		 		 	  		   	  			  	
    # Note that ALL of these values will be set to different values by 			  		 			 	 	 		 		 	  		   	  			  	
    # the autograder! 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    start_date = dt.datetime(2009,1,1) 			  		 			 	 	 		 		 	  		   	  			  	
    end_date = dt.datetime(2010,1,1) 			  		 			 	 	 		 		 	  		   	  			  	
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM'] 	

    # For report
    #start_date = dt.datetime(2008,6,1) 			  		 			 	 	 		 		 	  		   	  			  	
    #end_date = dt.datetime(2009,6,1) 			  		 			 	 	 		 		 	  		   	  			  	
    #symbols = ['IBM', 'X', 'GLD', 'JPM'] 			  		 			 	 	 		 		 	  		   	  			  			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Assess the portfolio 			  		 			 	 	 		 		 	  		   	  			  	
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
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
    # This code WILL NOT be called by the auto grader 			  		 			 	 	 		 		 	  		   	  			  	
    # Do not assume that it will be called 			  		 			 	 	 		 		 	  		   	  			  	
    test_code() 			  		 			 	 	 		 		 	  		   	  			  	
