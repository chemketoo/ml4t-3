import numpy as np 		
import DTLearner as dl
import LinRegLearner as lrl		 	 	 		 		 	  		   	  			  	
import RTLearner as rt

class BagLearner(object): 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def __init__(self, learner, kwargs, bags, boost = False, verbose = False): 			  		 			 	 	 		 		 	  		   	  			  	
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost # NOT IMPLEMENTED

        # pass learner-specific args to learner constructors
        self.learner_group = [learner(**kwargs) for bag in range(self.bags)]

    def author(self): 			  		 			 	 	 		 		 	  		   	  			  	
        return 'gtusername' 

    def addEvidence(self,xdata, ydata): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Add training data to learner 			  		 			 	 	 		 		 	  		   	  			  	
        @param xdata: X values of data to add 			  		 			 	 	 		 		 	  		   	  			  	
        @param ydata: the Y training values 			  		 			 	 	 		 		 	  		   	  			  	
        """ 		
        # each bag gets a different random subset of data
        # call methods on each learner instance
        for bag in range(self.bags):
            randomSubset = np.random.choice(xdata.shape[0], size=xdata.shape[0], replace=True)
            randomX = xdata[randomSubset, :]
            randomY = ydata[randomSubset]
            self.learner_group[bag].addEvidence(randomX, randomY)

    def query(self, points): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Estimate a set of test points given the model we built. 			  		 			 	 	 		 		 	  		   	  			  	
        @param points: should be a numpy array with each row corresponding to a specific query. 			  		 			 	 	 		 		 	  		   	  			  	
        @returns the estimated values according to the saved model. 			  		 			 	 	 		 		 	  		   	  			  	
        """ 
        # for each bag query
        results = [self.learner_group[bag].query(points) for bag in range(self.bags)]
        # because it's bag learner, take the mean of the resulting column
        return np.mean(results, axis=0)
        	  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "the secret clue is 'zzyzx'" 			  		 			 	 	 		 		 	  		   	  			  	
