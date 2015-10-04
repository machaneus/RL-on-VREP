import math
import numpy as np
import cPickle as pickle

class ZeroDict(dict):
    def __getitem__(self, key):
        self.setdefault(key, 0)
        return dict.__getitem__(self, key)

class LinearApproximator:
    def __init__(self, actionSet, targetPos):
        
        self.actionSet = actionSet        
        self.weights = dict()
        
        for action in actionSet:
            self.weights[action] = np.zeros(3)
        
        self.targetPos = targetPos
        
    def __getitem__(self,stateActionPair):
        state = stateActionPair[0]
        action = stateActionPair[1]
        return self.calculateQValue(state,action)
    
    def f(self, state):
        
        f1 = abs(self.targetPos[0]-state[0])+abs(self.targetPos[1]-state[1])
        f2 = abs(math.atan2(self.targetPos[1]-state[1],self.targetPos[0]-state[0]) - (state[2]+state[5]))
        f3 = state[4]*f2#state[3]
        
        return np.array([f1,f2,f3])
        
    def calculateQValue(self, state, action):
        return np.dot(self.weights[action],self.f(state))
        
    def getBestActionMaxQValue(self, state):
        bestAction = None
        maxQValue=-10000000
        for action in self.actionSet:
            qValue=self.calculateQValue(state, action)
            if maxQValue<qValue:
                maxQValue=qValue
                bestAction = action
        
        return bestAction, maxQValue
    
    def updateWeights(self, state, action, newState, reward, discount, alpha):
        if newState==None:
            maxNextQValue = 0
        else:
            _,maxNextQValue = self.getBestActionMaxQValue(newState)
        #print "  Update tuple: ",[state,action,newState,reward]
        difference = (reward+discount*maxNextQValue)-self.calculateQValue(state,action)
        #print "  Difference: ",difference
        #print "  f: ", self.f(state)
        #print "  old weights[",action,"]: ", self.weights[action]
        self.weights[action] = self.weights[action] + alpha*difference*self.f(state)
        
    def saveWeights(self,filename="../data/weights.pkl"):
        with open(filename, 'wb') as output:
            pickle.dump(self.weights,output,pickle.HIGHEST_PROTOCOL)
            
    def loadWeights(self,filename="../data/weights.pkl"):
        with open(filename, 'rb') as input:
            self.weights = pickle.load(input)
        
        

