import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  	
import os 			  		 			 	 	 		 		 	  		   	  			  	
from util import get_data, plot_data 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
def compute_portvals(init_trades, start_val = 100000, commission=9.95, impact=0.005): 			  		 			 	 	 		 		 	  		   	  			  	
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

    # updated this for strat learner, removed strftime accesses
    # not really vectorized, but better.
    for day, row in init_trades.iterrows():
        shares = init_trades.at[day, sym]
        if shares == 0.0:
            continue
        cash = shares * prices_df.at[day, sym]
        
        transaction = commission + (cash * impact)
        trades_df.at[day, sym] = trades_df.at[day, sym] + shares
        trades_df.at[day, 'CASH'] = trades_df.at[day, 'CASH'] - cash - transaction

    # HOLDINGS DF 
    holdings_df = prices_df.copy()
    holdings_df.iloc[:,0:-1] = 0
    holdings_df.iloc[:,-1] = 1.0

    rows = holdings_df.shape[0]
    # cash at start
    holdings_df.iloc[0,-1] = start_val
    for day, row in prices_df.iterrows():
        # first day
        if day == holdings_df.iloc[0].name:
            #holdings_df.at[day, sym] = holdings_df.at[day, sym] + trades_df.at[day, sym]
            #holdings_df.at[day, 'CASH'] = start_val + trades_df.at[day, 'CASH']
            holdings_df.at[day] = holdings_df.loc[day] + trades_df.loc[day]
        else:
            # not always the previous date timewise
            idx = holdings_df.index.get_loc(day)  
            #holdings_df.at[day, sym] = holdings_df.iloc[idx - 1][sym] + trades_df.at[day, sym]
            #holdings_df.at[day, 'CASH'] = holdings_df.iloc[idx - 1]['CASH'] + trades_df.at[day, 'CASH']
            holdings_df.loc[day] = holdings_df.iloc[idx -1] + trades_df.loc[day]
    # VALUE DF (prices * holdings)
    values_df = prices_df * holdings_df

    # PORTVAL DF (sum of each value row)
    portvals = pd.DataFrame(values_df.sum(axis=1))			  		 			 	 	 		 		 	  		   	  			  	
    return portvals 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	 	  		 			 	 	 		 		 	  		   	  			  	
def author():
    return 'gtusername'
		  		 			 	 	 		 		 	  		   	  			  	
if __name__ == "__main__": 			  		 			 	 	 		 		 	  		   	  			  				  		 			 	 	 		 		 	  		   	  			  	
    pass



    
