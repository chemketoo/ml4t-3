"""MC2-P1: Market simulator. 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  	
import os 			  		 			 	 	 		 		 	  		   	  			  	
from util import get_data, plot_data 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005): 			  		 			 	 	 		 		 	  		   	  			  	
    # this is the function the autograder will call to test your code 			  		 			 	 	 		 		 	  		   	  			  	
    # NOTE: orders_file may be a string, or it may be a file object. Your 			  		 			 	 	 		 		 	  		   	  			  	
    # code should work correctly with either input 			  		 			 	 	 		 		 	  		   	  			  	  		 			 	 	 		 		 	  		   	  			  	
    
    #ORDERS DF
    orders_df = pd.read_csv(orders_file, parse_dates=True, na_values=['nan'])
    orders_df.sort_values(by=['Date'],inplace=True)

    # PRICES DF
    syms = orders_df['Symbol'].unique().tolist()
    dates = pd.date_range(orders_df.iloc[0]['Date'], orders_df.iloc[-1]['Date'])
    prices_df = get_data(syms, dates, addSPY=False, colname = 'Adj Close')
    
    prices_df = prices_df.dropna(how='all')
    prices_df = prices_df.fillna(method='ffill')
    prices_df = prices_df.fillna(method='bfill')
    prices_df['CASH'] = 1.0

    # TRADES DF 
    # Init all to zero except cash
    trades_df = prices_df.copy()
    trades_df.iloc[:,:] = 0
    trades_df.iloc[:,-1] = 0.0
    
    rows = orders_df.shape[0]

    for i in range(rows):
        date = orders_df.loc[i]['Date']
        sym = orders_df.loc[i]['Symbol']
        orderType = orders_df.loc[i]['Order']
        shares = orders_df.loc[i]['Shares']
        cash = shares * prices_df.loc[date][sym]

        transaction = commission + (cash * impact)

        if orderType == 'BUY':
            trades_df.loc[date][sym] = trades_df.loc[date][sym] + shares
            trades_df.loc[date]['CASH'] = trades_df.loc[date]['CASH'] - cash - transaction
        elif orderType == 'SELL':
            trades_df.loc[date][sym] = trades_df.loc[date][sym] - shares
            trades_df.loc[date]['CASH'] = trades_df.loc[date]['CASH'] + cash - transaction
    print(trades_df)
    # HOLDINGS DF 
    holdings_df = prices_df.copy()
    holdings_df.iloc[:,0:-1] = 0
    holdings_df.iloc[:,-1] = 1.0

    rows = holdings_df.shape[0]
    # cash at start
    holdings_df.iloc[0,-1] = start_val
    for i in range(0, rows):
        date = holdings_df.iloc[i].name.strftime('%Y-%m-%d')
        if i == 0:
            holdings_df.loc[date] = holdings_df.loc[date] + trades_df.loc[date]
        else:
            holdings_df.loc[date] = holdings_df.iloc[i -1] + trades_df.loc[date]

    # VALUE DF (prices * holdings)
    values_df = prices_df * holdings_df

    # PORTVAL DF (sum of each value row)
    portvals = pd.DataFrame(values_df.sum(axis=1))			  		 			 	 	 		 		 	  		   	  			  	
    return portvals 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
def test_code(): 			  		 			 	 	 		 		 	  		   	  			  	
    # this is a helper function you can use to test your code 			  		 			 	 	 		 		 	  		   	  			  	
    # note that during autograding his function will not be called. 			  		 			 	 	 		 		 	  		   	  			  	
    # Define input parameters 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    #of = "./orders/orders-02.csv" 	
    #of = "./orders/orders-short.csv"	
    #of = "./additional_orders/orders.csv"	 
    of = "./orders/orders-01.csv" 		 			 	 	 		 		 	  		   	  			  	
    sv = 1000000 
    c = 0
    imp = 0			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Process orders 			  		 			 	 	 		 		 	  		   	  			  	
    #portvals = compute_portvals(orders_file = of, start_val = sv) 	
    portvals = compute_portvals(orders_file = of, start_val = sv, commission=c, impact=imp) 		  		 			 	 	 		 		 	  		   	  			  	
    if isinstance(portvals, pd.DataFrame): 			  		 			 	 	 		 		 	  		   	  			  	
        portvals = portvals[portvals.columns[0]] # just get the first column 			  		 			 	 	 		 		 	  		   	  			  	
    else: 			  		 			 	 	 		 		 	  		   	  			  	
        "warning, code did not return a DataFrame" 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Get portfolio stats 			  		 			 	 	 		 		 	  		   	  			  	
    # Here we just fake the data. you should use your code from previous assignments. 			  		 			 	 	 		 		 	  		   	  			  	
    dates = portvals.index.values
    start_date = np.datetime64(dates[0],'D')		  		 			 	 	 		 		 	  		   	  			  	
    end_date = np.datetime64(dates[-1], 'D') 	
    cum_ret = (portvals[-1] / portvals[0]) - 1

    #normed = portvals / portvals[0]
    daily_returns = portvals / portvals.shift(1) - 1
    avg_daily_ret = daily_returns[1:].mean()
    std_daily_ret = daily_returns[1:].std()	
    sharpe_ratio =   np.sqrt(252) * (daily_returns[1:] - 0.0).mean() / std_daily_ret	 			 	 	 		 			 	 	 		 		 	  		   	  			  	
   
    cum_ret_SPY = 0
    avg_daily_ret_SPY = 0
    std_daily_ret_SPY = 0
    sharpe_ratio_SPY = 	0		  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # Compare portfolio against $SPX 			  		 			 	 	 		 		 	  		   	  			  	
    print "Date Range: {} to {}".format(start_date, end_date) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio) 			  		 			 	 	 		 		 	  		   	  			  	
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Cumulative Return of Fund: {}".format(cum_ret) 			  		 			 	 	 		 		 	  		   	  			  	
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Standard Deviation of Fund: {}".format(std_daily_ret) 			  		 			 	 	 		 		 	  		   	  			  	
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Average Daily Return of Fund: {}".format(avg_daily_ret) 			  		 			 	 	 		 		 	  		   	  			  	
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY) 			  		 			 	 	 		 		 	  		   	  			  	
    print 			  		 			 	 	 		 		 	  		   	  			  	
    print "Final Portfolio Value: {}".format(portvals[-1]) 			  		 			 	 	 		 		 	  		   	  			  	

def author():
    return 'gtusername'
		  		 			 	 	 		 		 	  		   	  			  	
if __name__ == "__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    test_code() 			  		 			 	 	 		 		 	  		   	  			  	
