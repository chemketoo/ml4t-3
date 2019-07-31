""" 			  		 			 	 	 		 		 	  		   	  			  	
Template for implementing QLearner  (c) 2015 Tucker Balch 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
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
import random as rand 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
class QLearner(object): 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False): 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
        self.verbose = verbose 			  		 			 	 	 		 		 	  		   	  			  	
        self.num_actions = num_actions 	
        self.num_states = num_states	  		 			 	 	 		 		 	  		   	  			  	
        self.s = 0 			  		 			 	 	 		 		 	  		   	  			  	
        self.a = 0 	
        self.rar = rar
        self.radr = radr
        self.alpha = alpha
        self.gamma = gamma
        self.dyna = dyna

        self.query_count = 0
        self.Q = np.random.uniform(-1, 1, size=(num_states, num_actions))
        if self.dyna != 0:
            # init TCount and R
            # row = s, col = a, depth = s'
            self.TC = np.ndarray(shape=(num_states, num_actions, num_states))
            self.TC.fill(.00001) # small value to avoid divide by zero
            self.T = self.TC / self.TC.sum(axis=2, keepdims=True)
            self.R = np.ndarray(shape=(num_states, num_actions))
            self.R.fill(-1.0)		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def querysetstate(self, s): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Update the state without updating the Q-table 			  		 			 	 	 		 		 	  		   	  			  	
        @param s: The new state 			  		 			 	 	 		 		 	  		   	  			  	
        @returns: The selected action 			  		 			 	 	 		 		 	  		   	  			  	
        """ 		  		 			 	 	 		 		 	  		   	  			  	
        self.s = s 			  		 			 	 	 		 		 	  		   	  			  	
        
        # ignore selected action and return random one
        #if rand.uniform(0.0, 1.0) <= self.rar:
        if rand.random() <= self.rar:
            action = rand.randint(0,self.num_actions - 1) 		 			 	 	 		 		 	  		   	  			  	
        else:
            # action to take
            action = np.argmax(self.Q[s, :])
        if self.verbose: 
            print "s =", s,"a =",action	 			 	 	 		 		 	  		   	  			 
        self.a = action	 			  		 			 	 	 		 		 	  		   	  			  	
        return action 			  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
    def query(self,s_prime,r): 			  		 			 	 	 		 		 	  		   	  			  	
        """ 			  		 			 	 	 		 		 	  		   	  			  	
        @summary: Update the Q table and return an action 			  		 			 	 	 		 		 	  		   	  			  	
        @param s_prime: The new state 			  		 			 	 	 		 		 	  		   	  			  	
        @param r: The reward 			  		 			 	 	 		 		 	  		   	  			  	
        @returns: The selected action 			  		 			 	 	 		 		 	  		   	  			  	
        """
        # ignore selected action and return random one
        if rand.random() <= self.rar:
            action = rand.randint(0,self.num_actions - 1) 
		 			 	 	 		 		 	  		   	  			  	
        else:
            action = np.argmax(self.Q[s_prime, :])
        # update rar according to decay rate
        self.rar =  self.rar * self.radr
        # Update the Q table
        self.Q[self.s, self.a] = ((1 - self.alpha) * self.Q[self.s, self.a]) + (self.alpha * (r + (self.gamma * self.Q[s_prime, action])))
            
        if self.verbose:
            print "s =", s_prime,"a =",action,"r =",r 

        self.query_count += 1
        if self.dyna != 0 and self.query_count > 15:
            # Learn Models of T and R
            self.TC[self.s, self.a, s_prime] += 1
            self.R[self.s, self.a] = ((1 - self.alpha) * self.R[self.s, self.a]) + (self.alpha * r)

            # Probabilities
            self.T[self.s, self.a, :] = self.TC[self.s, self.a, :] / self.TC[self.s, self.a, :].sum()

            # random states and actions
            d_states = np.random.randint(self.num_states, size=(self.dyna,))
            d_actions = np.random.randint(self.num_actions, size=(self.dyna,))
            
            # Hallucinate
            for i in range(self.dyna):
                #Random state, random action
                d_state = d_states[i]
                d_action = d_actions[i]
                d_s_prime = np.argmax(np.random.multinomial(1, self.T[d_state, d_action, :]))
                d_r = self.R[d_state, d_action]
                self.Q[d_state, d_action] = ((1 - self.alpha) * self.Q[d_state, d_action]) + (self.alpha * (d_r + (self.gamma * np.max(self.Q[d_s_prime,:]))))

        self.s = s_prime
        self.a = action	 			 	 	 		 		 	  		   	  			  	
        return action 	

    def author(self): 
        return 'gtusername'	  		 			 	 	 		 		 	  		   	  			  	
 			  		 			 	 	 		 		 	  		   	  			  	
if __name__=="__main__": 			  		 			 	 	 		 		 	  		   	  			  	
    print "Remember Q from Star Trek? Well, this isn't him" 			  		 			 	 	 		 		 	  		   	  			  	
