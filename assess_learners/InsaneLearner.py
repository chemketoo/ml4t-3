import numpy as np 		
import LinRegLearner as lrl	
import BagLearner as bl	 	 	 		 		 	  		   	  			  	
class InsaneLearner(object): 			  		 			 	 	 		 		 	  		   	  			  	 			  		 			 	 	 		 		 	  		   	  			  	
    def __init__(self, learner=lrl.LinRegLearner, kwargs={}, bags=20, verbose=False): 			  		 			 	 	 		 		 	  		   	  			  	
        self.verbose = verbose
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.learner_group = [bl.BagLearner(learner=self.learner, kwargs=self.kwargs, bags=self.bags) for i in range(self.bags)]
    def author(self): 			  		 			 	 	 		 		 	  		   	  			  	
        return 'gtusername' 
    def addEvidence(self,xdata, ydata): 			  		 			 	 	 		 		 	  		   	  			  		
        evidenceList = [self.learner_group[bag].addEvidence(xdata, ydata) for bag in range(self.bags)]
    def query(self, points): 			  		 			 	 	 		 		 	  		   	  			  	
        results = [self.learner_group[bag].query(points) for bag in range(self.bags)]
        return np.mean(results, axis=0)   	  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "the secret clue is 'zzyzx'" 			  		 			 	 	 		 		 	  		   	  			  	
