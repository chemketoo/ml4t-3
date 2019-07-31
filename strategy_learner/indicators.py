import pandas as pd 			  		 			 	 	 		 		 	  		   	  			  	
import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
import datetime as dt 			  		 			 	 	 		 		 	  		   	  			  				  		 			 	 	 		 		 	  		   	  			  	
from util import plot_data 
import matplotlib.pyplot as plt	

def sma(prices, lookback):
    # price/sma ratio
    n_prices = prices / prices.values[0]
    sma = n_prices.rolling(window=lookback, min_periods=lookback).mean()
    ratio_sma = n_prices / sma
    '''
    Commenting out for StrategyLearner
    fig, axes = plt.subplots(2, 1, sharex=True)
    axes[0].plot(n_prices, color='blue', label='Price')
    axes[0].plot(sma, color='green', label='SMA')
    axes[0].legend()
    axes[0].grid()

    axes[1].plot(ratio_sma, color='blue', label='Price / SMA')
    axes[1].legend(loc='lower left')
    axes[1].grid()
    plt.tight_layout()
    fig.suptitle('SMA')
    fig.subplots_adjust(top=.9)
    plt.savefig('sma.png')
    '''
    return ratio_sma

def bollinger_percentage(prices, window):
    # normalize and set to zero
    n_prices = prices / prices.values[0]
    bb = n_prices.copy()
    bb[:] = 0

    # stats
    sma = n_prices.rolling(window=window, min_periods=window).mean()
    
    stdev = n_prices.rolling(window=window, min_periods=window).std()
    bb_top = sma + (2 * stdev)
    bb_bottom = sma - (2 * stdev)
    # as shown in lectures, use percentage to know when we cross
    bb_percentage = (n_prices - bb_bottom) / (bb_top - bb_bottom)
    
    '''
    Commenting out for StrategyLearner
    # visualization-2 plots 
    fig, axes = plt.subplots(2, 1, sharex=True)
    axes[0].plot(n_prices, color='blue', label='Price')
    axes[0].plot(bb_top, color='red', label='Top')
    axes[0].plot(bb_bottom, color='green', label='Bottom')
    axes[0].legend()
    axes[0].grid()

    axes[1].plot(bb_percentage, label='BB Ratio')
    axes[1].legend()
    axes[1].grid()

    plt.tight_layout()
    fig.suptitle('Bollinger Bands')
    fig.subplots_adjust(top=.9)
    plt.savefig('bollinger.png')
    '''
    return bb_percentage

def momentum(prices, lookback):
    # normalize and set to zero
    n_prices = prices / prices.values[0]
    momentum_val = n_prices / n_prices.shift(lookback) - 1
    '''
    Commenting out for StrategyLearner
    fig, axes = plt.subplots(2, 1, sharex=True)
    axes[0].plot(n_prices, color='blue', label='Price')
    axes[0].legend()
    axes[0].grid()

    axes[1].plot(momentum_val, color='blue', label='Momentum')
    axes[1].legend(loc='lower left')
    axes[1].grid()
    plt.tight_layout()
    fig.suptitle('Price and Momentum')
    fig.subplots_adjust(top=.9)
    plt.savefig('momentum.png')
    '''
    return momentum_val

def author():
    return 'gtusername'