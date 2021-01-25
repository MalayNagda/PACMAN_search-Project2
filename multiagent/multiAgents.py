# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	#print 'successorGameState',successorGameState
	#print '_________________________________'
	#print 'newPos',newPos
	#print '_________________________________'
	#print 'newFood',newFood
	#print '_________________________________'
	#print 'newGhostStates',newGhostStates
	#print '_________________________________'
	#print 'newScaredTimes',newScaredTimes
	#print '_________________________________'

        "*** YOUR CODE HERE ***"
	closest=[]
	score=0
	for ghost in newGhostStates:
		closest.append(util.manhattanDistance(newPos,ghost.getPosition()))
	closest_ghost=min(closest)
	if closest_ghost:
		score= score -(100/closest_ghost)
	else:
		score= score - 10000
	food_remaining=newFood.asList()
	closest=[]
	if food_remaining:	
		for food in food_remaining:
			closest.append(util.manhattanDistance(newPos,food))
		closest_food= min(closest)
		score=score-closest_food
	else:
		score= score
	score=score - (100*len(food_remaining))
	
	return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
	def minimax(state, agent_number, depth):
		#print state
            	if agent_number== state.getNumAgents():
                	if depth== self.depth:
                    		return self.evaluationFunction(state)
                	else:
				depth=depth+ 1
                    		return minimax(state, 0, depth)
            	else:
                	directions= state.getLegalActions(agent_number)
                	if len(directions)== 0:
                    		return self.evaluationFunction(state)
			next= []
			for direction in directions:
				next.append(minimax(state.generateSuccessor(agent_number, direction), agent_number + 1, depth))
			#print next
                	if agent_number== 0:
                    		return max(next)
                	else:
                    		return min(next)
	moves1= gameState.getLegalActions(0)
	scores=[]
	moves2=[]
	for m in moves1:
		scores.append(minimax(gameState.generateSuccessor(0, m), 1, 1))
		moves2.append(m)
	sc_idx=scores.index(max(scores))
        return moves2[sc_idx]
	
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.
        """
        "*** YOUR CODE HERE ***"
        def pruner(state, agent_number, depth, alpha, beta):
            if state.isLose() or state.isWin() or depth== self.depth:
                return self.evaluationFunction(state)
            if agent_number== 0:
                return max_layer(state, agent_number, depth, alpha, beta)
            elif agent_number> 0: 
                return min_layer(state, agent_number, depth, alpha, beta)

        def max_layer(state, agent_number, depth, alpha, beta):  
            v= -100000
            for directions in state.getLegalActions(agent_number):
                v= max(v, pruner(state.generateSuccessor(agent_number, directions), 1, depth, alpha, beta))
                if v> beta:
                    return v
                alpha= max(alpha, v)
            return v

        def min_layer(state, agent_number, depth, alpha, beta):
            v= 100000
            next_agent= agent_number+ 1 
            if state.getNumAgents()== next_agent:
                next_agent= 0
            if next_agent== 0:
                depth+= 1
            for directions in state.getLegalActions(agent_number):
                v = min(v, pruner(state.generateSuccessor(agent_number, directions), next_agent, depth, alpha, beta))
                if v< alpha:
                    return v
                beta= min(beta, v)
            return v

        alpha, beta,v= -100000, 100000, -100000
	direction= None
        for directions in gameState.getLegalActions(0):
            score = pruner(gameState.generateSuccessor(0, directions), 1, 0, alpha, beta)
            if score > v:
                v = score
                direction = directions
            if v > beta:
                return v
            alpha = max(alpha, v)
        return direction
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(state, agentIndex, depth):
            if agentIndex == state.getNumAgents():
                if depth == self.depth:
                    return self.evaluationFunction(state)
                else:
		    depth= depth + 1
                    return expectimax(state, 0, depth)
            else:
                directions = state.getLegalActions(agentIndex)
                if len(directions) == 0:
                    return self.evaluationFunction(state)
		next=[]
		for d in directions:
			next.append(expectimax(state.generateSuccessor(agentIndex, d), agentIndex + 1, depth))
		#print next
                if agentIndex == 0:
		    #print max(next)
                    return max(next)
                else:
	 	    expecti= sum(next)/ len(next)
                    return expecti
	moves1= gameState.getLegalActions(0)
	scores=[]
	moves2=[]
	for m in moves1:
		scores.append(expectimax(gameState.generateSuccessor(0, m), 1, 1))
		moves2.append(m)
	sc_idx=scores.index(max(scores))
        return moves2[sc_idx]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    closest=[]
    score=0
    for ghost in newGhostStates:
	closest.append(util.manhattanDistance(newPos,ghost.getPosition()))
    closest_ghost=min(closest)
    if closest_ghost:
	score= score -(100/closest_ghost)
    else:
	score= score - 1000
    food_remaining=newFood.asList()
    closest=[]
    if food_remaining:	
	for food in food_remaining:
		closest.append(util.manhattanDistance(newPos,food))
	closest_food= min(closest)
	score=score-closest_food
    else:
    	score= score
    if newScaredTimes[0] != 0:
    	score= score+ float(50000/closest_ghost)
    score= score- 1000*len(food_remaining)
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

