import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  	
import os 			  		 			 	 	 		 		 	  		   	  			  	
from util import get_data, plot_data 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
def compute_portvals(init_trades, start_val = 1000000, commission=9.95, impact=0.005): 			  		 			 	 	 		 		 	  		   	  			  	
    syms = list(init_trades.columns)
    # for this project, just one symbol
    sym = syms[0]
    
    dates = pd.date_range(init_trades.iloc[0].name.strftime('%Y-%m-%d'), init_trades.iloc[-1].name.strftime('%Y-%m-%d'))

    # PRICES DF
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
    
    rows = init_trades.shape[0]

    for i in range(rows):
        date = init_trades.iloc[i].name.strftime('%Y-%m-%d')
        # at is faster than loc for scalar (single) value
        shares = init_trades.at[init_trades.index[i], sym]
        if shares == 0.0:
            continue
        cash = shares * prices_df.loc[date][sym]

        transaction = commission + (cash * impact)
        trades_df.loc[date][sym] = trades_df.loc[date][sym] + shares
        trades_df.loc[date]['CASH'] = trades_df.loc[date]['CASH'] - cash - transaction

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
 			  		 			 	 	 		 		 	  		   	  			  	 	  		 			 	 	 		 		 	  		   	  			  	
def author():
    return 'gtusername'
		  		 			 	 	 		 		 	  		   	  			  	
if __name__ == "__main__": 			  		 			 	 	 		 		 	  		   	  			  				  		 			 	 	 		 		 	  		   	  			  	
    pass



    