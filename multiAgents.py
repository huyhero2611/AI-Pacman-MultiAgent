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
        newPos = successorGameState.getPacmanPosition() #pacman position after moving 
        newFood = successorGameState.getFood() #remain food
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # check anydots was eaten
        if successorGameState.isWin():
          return 1000000

        closestFood = min([manhattanDistance(newPos, food) for food in newFood.asList()])

        # check if ghost no scare and position between ghost and pacman < 2 => don't this action
        for ghost in newGhostStates:
          if ghost.scaredTimer == 0 and manhattanDistance(ghost.getPosition(), newPos) < 2: 
            return -1000000
        return successorGameState.getScore() * 10.0 + 1.0 / closestFood

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
        actions = gameState.getLegalActions(0)
        return max(actions, key = lambda x: self.minimax_search(gameState.generateSuccessor(0, x), 1))
        
    def minimax_search(self, gameState, turn): # moi khi agent chuyen dong, turn++
      numAgents = gameState.getNumAgents()
      agentIndex = turn % numAgents
      depth = turn // numAgents

      if gameState.isWin() or gameState.isLose() or depth == self.depth:
        return self.evaluationFunction(gameState)
      actions = gameState.getLegalActions(agentIndex) # list action of an Agent
      # them 1 mang tinh cac gia tri cua node con cua node do
      evals = [self.minimax_search(gameState.generateSuccessor(agentIndex, action), turn + 1) for action in actions]

      if agentIndex > 0: # is ghost
        return min(evals)
      return max(evals) # is pacman
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha, beta = -1000000, 1000000
        actions = gameState.getLegalActions(0)
        vals = []
        for action in actions:
          v = self.alphabeta_search(gameState.generateSuccessor(0, action), 1, alpha, beta)
          alpha = max(alpha, v)
          vals.append(v)
        for i in range(len(vals)):
          if alpha == vals[i]:
            return actions[i]
        

    def alphabeta_search(self, gameState, turn, alpha, beta):
      numAgents = gameState.getNumAgents()
      agentIndex = turn % numAgents
      depth = turn // numAgents

      if gameState.isWin() or gameState.isLose() or depth == self.depth:
        return self.evaluationFunction(gameState)

      actions = gameState.getLegalActions(agentIndex)
      if agentIndex == 0: # is ghost
        v = -1000000
      else: # is pacman
        v = 1000000
      for action in actions:
        successor = gameState.generateSuccessor(agentIndex, action)
        if (agentIndex > 0): # min value
          v = min(v, self.alphabeta_search(successor, turn + 1, alpha, beta))
          if v < alpha:
            return v
          beta = min(beta, v)
        else:
          v = max(v, self.alphabeta_search(successor, turn + 1, alpha, beta))
          if v > beta:
            return v
          alpha = max(alpha, v)
      return v

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
      actions = gameState.getLegalActions(0)
      return max(actions, key = lambda x: self.expectimax_search(gameState.generateSuccessor(0, x), 1))
 # muc dich: expectimax co the nghi ghost khong phai la toi uu => xac suat de thang trapped ~ 50% (vi no coi ghost nao cung nhu nhau)
    def expectimax_search(self, gameState, turn):
      numAgents = gameState.getNumAgents()
      agentIndex = turn % numAgents
      depth = turn // numAgents

      if gameState.isWin() or gameState.isLose() or depth == self.depth:
        return self.evaluationFunction(gameState)
      actions = gameState.getLegalActions(agentIndex)
      evals = [self.expectimax_search(gameState.generateSuccessor(agentIndex, action), turn + 1) for action in actions]

      if agentIndex > 0:
        return sum(evals) * 1.0 / len(evals) 
      return max(evals)
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    if currentGameState.isWin():
      return 1000000
    if currentGameState.isLose():
      return -1000000

    foods = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    pacmanPosition = currentGameState.getPacmanPosition()

    closestFood = min(manhattanDistance(pacmanPosition, food) for food in foods.asList())
    cover_me = sum([(manhattanDistance(pacmanPosition, ghost.getPosition()) < 3) for ghost in ghostStates]) # tinh so ghost cach pacman voi khoang cach < 3
    scare_me = sum([(ghost.scaredTimer == 0) for ghost in ghostStates]) # so ghost ma hien tai no k bi so

    return currentGameState.getScore() * 10.0 + 1.0 / closestFood + 1.0 * cover_me + 1.0 / (scare_me + 0.01)
# Abbreviation
better = betterEvaluationFunction

