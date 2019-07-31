""" 			  		 			 	 	 		 		 	  		   	  			  	
Test a learner.  (c) 2015 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
import math 			  		 			 	 	 		 		 	  		   	  			  	
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt			
import BagLearner as bl  	
import InsaneLearner as it	 			 	 	 		 		 	  		   	  			  	
import sys 			  
from util import get_learner_data_file	
import matplotlib.pyplot as plt
import pandas as pd		
import time
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    if len(sys.argv) != 2: 			  		 			 	 	 		 		 	  		   	  			  	
        print "Usage: python testlearner.py <filename>" 			  		 			 	 	 		 		 	  		   	  			  	
        sys.exit(1) 
    datafile = sys.argv[1]
    with get_learner_data_file(datafile) as f: 			  		 			 	 	 		 		 	  		   	  			  	
        data = np.genfromtxt(f,delimiter=',') 			  		 			 	 	 		 		 	  		   	  			  	
        # Skip the date column and header row if we're working on Istanbul data 			  		 			 	 	 		 		 	  		   	  			  	
        if datafile == 'Istanbul.csv': 			  		 			 	 	 		 		 	  		   	  			  	
            data = data[1:,1:]
	 	 	 		 		 	  		   	  			  	
    # compute how much of the data is training and testing 			  		 			 	 	 		 		 	  		   	  			  	
    train_rows = int(0.6* data.shape[0]) 			  		 			 	 	 		 		 	  		   	  			  	
    test_rows = data.shape[0] - train_rows 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    # separate out training and testing data 			  		 			 	 	 		 		 	  		   	  			  	
    trainX = data[:train_rows,0:-1] 			  		 			 	 	 		 		 	  		   	  			  	
    trainY = data[:train_rows,-1] 			  		 			 	 	 		 		 	  		   	  			  	
    testX = data[train_rows:,0:-1] 			  		 			 	 	 		 		 	  		   	  			  	
    testY = data[train_rows:,-1] 			  		 			 	 	 		 		 	  		   	  			  			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  		  		 			 	 	 		 		 	  		   	  			  	
    # DTLEARNER create a learner and train it 			  		 			 	 	 		 		 	  		   	  			  	
    # Q1, create multiple learners with increasing leaf sizes
    # evaluate RMSE, then plot

    q1X = np.linspace(1, 50, num=5)
    rmse_in = []
    rmse_out = []
    predY = None
    for i in q1X:
        q1learner = dt.DTLearner(leaf_size=i,verbose = True) # create a DTLearner 			  		 			 	 	 		 		 	  		   	  			  	
        q1learner.addEvidence(trainX, trainY) # train it
    
        #eval in sample
        predY = q1learner.query(trainX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
        rmse_in.append(math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]))			  		 			 	 	 		 		 	  		   	  			  				  		 			 	 	 		 		 	  		   	  			  				  		 			 	 	 		 		 	  		   	  			  				  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        # eval out of sample 			  		 			 	 	 		 		 	  		   	  			  	
        predY = q1learner.query(testX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
        rmse_out.append(math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]))			  		 			 	 	 		 		 	  		   	  			  	

    #Plot
    plt.clf()
    plt.plot(q1X, rmse_in, label="In-Sample Error")
    plt.plot(q1X, rmse_out, label="Out-of-Sample Error")
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.legend()
    plt.savefig('Q1_DTL_RMSE.png')

    #Q2 Use bagging with DTLearner and increase leaf size. Fixed bag size

    q2X = np.linspace(1, 50, num=5)
    q2_rmse_in = []
    q2_rmse_out = []
    for i in q2X:
        predY = None
        q2learner = bl.BagLearner(learner=dt.DTLearner, kwargs={"leaf_size":i}, bags=20, verbose = False) # create a DTLearner 		
        q2learner.addEvidence(trainX, trainY) # train it
    
        #eval in sample
        predY = q2learner.query(trainX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
        q2_rmse_in.append(math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0]))			  		 			 	 	 		 		 	  		   	  			  				  		 			 	 	 		 		 	  		   	  			  				  		 			 	 	 		 		 	  		   	  			  				  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        # evaluate out of sample 			  		 			 	 	 		 		 	  		   	  			  	
        predY = q2learner.query(testX) # get the predictions 			  		 			 	 	 		 		 	  		   	  			  	
        q2_rmse_out.append(math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0]))			  		 			 	 	 		 		 	  		   	  			  	

    #Plot
    plt.clf()
    plt.plot(q2X, q2_rmse_in, label="In-Sample Error")
    plt.plot(q2X, q2_rmse_out, label="Out-of-Sample Error")
    plt.xlabel('Leaf Size')
    plt.ylabel('RMSE')
    plt.legend()
    plt.savefig('Q2_BL_RMSE.png')

    #Q3 compare DTLearner and RTLearner, two quantitative measures
    # try time difference between learning and query as one measure
    # MSE as the other
    rt_train_time = []
    dt_train_time = []
    rt_query_time = []
    dt_query_time = []
    rt_mse_in = []
    rt_mse_out = []
    dt_mse_in = []
    dt_mse_out = []
    q3X = np.linspace(1, 50, num=5)
    for i in q3X:
        predY = None
        rtlearner = rt.RTLearner(leaf_size=i,verbose = True) # create a RTLearner 			  		 			 	 	 		 		 	  		   	  			  	
        rt_train_start = time.time()
        rtlearner.addEvidence(trainX, trainY) # train it 			  		  		 			 	 	 		 		 	  		   	  			  	
        rt_train_stop = time.time()
        rt_train_time.append(rt_train_stop - rt_train_start)

        #MSE In sample
        predY = rtlearner.query(trainX)
        rt_mse_in.append(((trainY - predY)**2).mean())

        rt_query_start = time.time()
        predY = rtlearner.query(testX)
        rt_query_stop = time.time()
        rt_query_time.append(rt_query_stop - rt_query_start)
        #MSE Out sample
        rt_mse_out.append(((testY - predY)**2).mean())

        dtlearner = dt.DTLearner(leaf_size=i,verbose = True) # create a RTLearner 			  		 			 	 	 		 		 	  		   	  			  	
        dt_train_start = time.time()
        dtlearner.addEvidence(trainX, trainY) # train it 			  		  		 			 	 	 		 		 	  		   	  			  	
        dt_train_stop = time.time()
        dt_train_time.append(dt_train_stop - dt_train_start)

        #MSE In sample
        predY = dtlearner.query(trainX)
        dt_mse_in.append(((trainY - predY)**2).mean())

        dt_query_start = time.time()
        predY = dtlearner.query(testX)
        dt_query_stop = time.time()
        dt_query_time.append(dt_query_stop - dt_query_start)
        # MSE Out sample
        dt_mse_out.append(((testY - predY)**2).mean())


    # Plot
    plt.clf()
    plt.plot(q3X, rt_train_time, label="RT Training Time")
    plt.plot(q3X, dt_train_time, label="DT Training Time")
    plt.plot(q3X, rt_query_time, label="RT Query Test Time")
    plt.plot(q3X, dt_query_time, label="DT Query Test Time")
    plt.xlabel('Leafs')
    plt.ylabel('Training Time')
    plt.legend()
    plt.savefig('Q3_Time.png')

    plt.clf()
    plt.plot(q3X, rt_mse_in, label="RT MSE In Sample")
    plt.plot(q3X, dt_mse_in, label="DT MSE In Sample")
    plt.plot(q3X, rt_mse_out, label="RT MSE Out Sample")
    plt.plot(q3X, dt_mse_out, label="DT MSE Out Sample")
    plt.xlabel('Leafs')
    plt.ylabel('MSE')
    plt.tight_layout()
    plt.legend()
    plt.savefig('Q3_MSE.png')
