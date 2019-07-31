import numpy as np 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
class DTLearner(object): 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def __init__(self, leaf_size = 1, verbose = False): 			  		 			 	 	 		 		 	  		   	  			  	
        self.leaf_size = leaf_size
        self.verbose = verbose 
        self.model_coefs = np.empty(())

    def author(self): 			  		 			 	 	 		 		 	  		   	  			  	
        return 'gtusername' 

    def addEvidence(self,xdata, ydata): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Add training data to learner 			  		 			 	 	 		 		 	  		   	  			  	
        @param xdata: X values of data to add 			  		 			 	 	 		 		 	  		   	  			  	
        @param ydata: the Y training values 			  		 			 	 	 		 		 	  		   	  			  	
        """ 		
        self.model_coefs = self.build_tree(xdata, ydata)
        return self.model_coefs

    def build_tree(self, xdata, ydata):
        """
        @summary: Recursively build tree for model
        @param xdata: X values
        @param ydata: Y values
        """
        # Represents terminal leafs
        leaf = np.array(([-1, ydata[0], np.nan, np.nan],))

        # one row in set or all y data is the same, return leaf
        if xdata.shape[0] <= self.leaf_size or np.unique(ydata).size == 1:
            return leaf

        # calc coefficients for all columns
        corrCoeffs = np.zeros(xdata.shape[1])
        for factor in range(corrCoeffs.shape[0]):
            corrCoeffs[factor] = abs(np.corrcoef(xdata[:, factor], ydata)[0, 1])
            if np.isnan(corrCoeffs[factor]):
                corrCoeffs[factor] = 0.0

        #index of factor with highest correlation
        factorIndex = np.argmax(corrCoeffs)
        splitValue = np.median(xdata[:, factorIndex])

        leftCondition = xdata[:, factorIndex] <= splitValue
        rightCondition = xdata[:, factorIndex] > splitValue

        # terminal condition
        if xdata[leftCondition].shape[0] == xdata.shape[0]:
            return leaf

        # traverse left and right trees
        left = self.build_tree(xdata[leftCondition], ydata[leftCondition])
        right = self.build_tree(xdata[rightCondition], ydata[rightCondition])
        root = np.array(([factorIndex, splitValue, 1, left.shape[0] + 1]),)
        return np.vstack((root, left, right))

    def query(self, points): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Estimate a set of test points given the model we built. 			  		 			 	 	 		 		 	  		   	  			  	
        @param points: should be a numpy array with each row corresponding to a specific query. 			  		 			 	 	 		 		 	  		   	  			  	
        @returns the estimated values according to the saved model. 			  		 			 	 	 		 		 	  		   	  			  	
        """ 
        # given points, return the prediction for each point
        # based on model

        results = []
        for p in points:
            r = 0
            (factor, splitVal) = self.model_coefs[r, 0:2]
            # while not a leaf and within range
            while int(factor) != -1 and r < len(self.model_coefs):
                r = int(r)
                # left condition, indices are relative
                if p[int(factor)] <= splitVal:
                    newRow = self.model_coefs[r, 2]
                    r += newRow
                # right condition
                else:
                    newRow = self.model_coefs[r, 3]
                    r += newRow
                if r < len(self.model_coefs):
                    (factor, splitVal) = self.model_coefs[int(r), 0:2]
            results.append(splitVal)
        return results
        	  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "the secret clue is 'zzyzx'" 			  		 			 	 	 		 		 	  		   	  			  	
