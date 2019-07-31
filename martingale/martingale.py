"""Assess a betting strategy. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
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
 			  		 			     			  	   		   	  			  	
import numpy as np 	
import pandas as pd
import matplotlib.pyplot as plt  
 			     			  	   		   	  			  	
def author(): 			  		 			     			  	   		   	  			  	
        return 'gtusername' # replace tb34 with your Georgia Tech username. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def gtid(): 			  		 			     			  	   		   	  			  	
	return 987654321 # replace with your GT ID number 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def get_spin_result(win_prob): 			  		 			     			  	   		   	  			  	
	result = False 			  		 			     			  	   		   	  			  	
	if np.random.random() <= win_prob:		  		 			     			  	   		   	  			  	
		result = True 			  		 			     			  	   		   	  			  	
	return result 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
def test_code(): 
	np.random.seed(gtid()) # do this only once
	experimentOne()
	experimentTwo()

def experimentOne():
	# 10 runs, Figure 1
	runs = 10
	winnings = np.zeros((1001, runs))
	for run in range(runs):			  		 			     			  	   		   	  			  	
		runWinnings = run_simulation()
		winnings[:, run] = runWinnings
	plot_data(winnings, 'fig1')

	# 1000 runs, mean value each spin, Figure 2
	runs = 1000
	winnings = np.zeros((1001, runs))
	for run in range(runs):
		runWinnings = run_simulation()
		winnings[:, run] = runWinnings
	plot_data_mean(winnings, 'fig2')
	# 1000 runs, median value each spin, Figure 3
	plot_data_median(winnings, 'fig3')

def experimentTwo():
	# 1000 runs, mean value each spin, Figure 4
	runs = 1000
	winnings = np.zeros((1001, runs))

	for run in range(runs):
		runWinnings = run_realistic_simulation()
		winnings[:, run] = runWinnings
	plot_data_mean(winnings, 'fig4')
	# 1000 runs, median value each spin, Figure 5
	plot_data_median(winnings, 'fig5')

	
def run_realistic_simulation():
	win_prob = 18/38.0 # set appropriately to the probability of a win 
	episode_winnings = 0
	spins = 1000
	currentSpin = 1
	won = False
	bet_amount = 1
	bank_roll = 256
	winningsSpins = np.zeros(1001)

	while episode_winnings > -256 and episode_winnings < 80 and currentSpin <= spins:
		won = get_spin_result(win_prob)
		if won:
			episode_winnings += bet_amount
			bank_roll += bet_amount
			bet_amount = 1
		else:
			episode_winnings -= bet_amount
			bank_roll -= bet_amount
			bet_amount = bet_amount * 2
			if bet_amount > bank_roll:
				bet_amount = bank_roll
		winningsSpins[currentSpin] = episode_winnings
		currentSpin += 1
	# fill forward:
	if episode_winnings == -256:
		winningsSpins[currentSpin:] = -256
	if episode_winnings == 80:
		winningsSpins[currentSpin:] = 80
	return winningsSpins
	

def run_simulation():
	win_prob = 18/38.0 # set appropriately to the probability of a win 			  		 			     			  	   		   	  			  				  		 			     			  	   		   	  			  	
	episode_winnings = 0
	spins = 1000
	currentSpin = 1
	won = False
	bet_amount = 1
	winningsSpins = np.zeros(1001)

	while episode_winnings < 80 and currentSpin <= spins:
		won = get_spin_result(win_prob)
		if won:
			episode_winnings += bet_amount
			bet_amount = 1
		else:
			episode_winnings -= bet_amount
			bet_amount = bet_amount * 2
		winningsSpins[currentSpin] = episode_winnings
		currentSpin += 1
	# fill forward:
	if episode_winnings == 80:
		winningsSpins[currentSpin:] = 80
	return winningsSpins

def plot_data(winnings, figNum):
	# columns represent separate datasets (column == run)
	plt.clf()
	data = pd.DataFrame(data=winnings)

	fig = plt.figure()
	plt.axis([0, 300, -256, 100])
	plt.title('Figure ' + figNum[-1])
	plt.xlabel('Spins')
	plt.ylabel('Winnings')
	lines = plt.plot(data)
	numRuns = len(lines)
	labels = []
	for i in range(numRuns):
		labels.append('run ' + str(i + 1))
	plt.legend(lines, labels)
	fig.savefig('./' + figNum + '.png')

def plot_data_mean(winnings, figNum):
	plt.clf()
	# take mean of each row (spin)
	data = pd.DataFrame(data=winnings)
	fig = plt.figure()

	meanDf = np.mean(data, axis=1)
	stdmean = np.std(data, axis=1)
	upper = meanDf + stdmean
	lower = meanDf - stdmean

	plt.axis([0, 300, -256, 100])
	plt.title('Figure ' + figNum[-1])
	plt.xlabel('Spins')
	plt.ylabel('Winnings')
	plt.plot(meanDf, label='Mean')
	plt.plot(upper, label='+Standard Dev')
	plt.plot(lower, label='-Standard Dev')
	plt.legend()
	fig.savefig('./' + figNum + '.png')

def plot_data_median(winnings, figNum):
	plt.clf()
	# take median of each row (spin)
	data = pd.DataFrame(data=winnings)
	fig = plt.figure()
	medianDf = np.median(data, axis=1)

	stdDev = np.std(data, axis=1)
	upper = medianDf + stdDev
	lower = medianDf - stdDev

	plt.axis([0, 300, -256, 100])
	plt.title('Figure ' + figNum[-1])
	plt.xlabel('Spins')
	plt.ylabel('Winnings')
	plt.plot(medianDf, label='Median')
	plt.plot(upper, label='+Standard Dev')
	plt.plot(lower, label='-Standard Dev')
	plt.legend()
	fig.savefig('./' + figNum + '.png')


if __name__ == "__main__": 			  		 			     			  	   		   	  			  	
    test_code() 			  		 			     			  	   		   	  			  	
