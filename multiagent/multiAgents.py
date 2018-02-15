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

        "*** YOUR CODE HERE ***"

        """ Initial Score value"""
        score = successorGameState.getScore();
        """ If food is left in the list will move pacman in direction of food reciprocal of nearest food distance"""
        if (len(newFood.asList()) > 0):
            minimum = min([manhattanDistance(newPos, food) for food in newFood.asList()])
            score += 10 / minimum;

        """ If ghost is present nearby need to move away from it : 20 double priority than food for pacman to live."""
        distance = manhattanDistance(newPos, newGhostStates[0].configuration.pos)
        if (distance > 0):
            score -= 20 / distance

        """ final score for making pacman move towards food and away from ghost."""
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
        #util.raiseNotDefined()
        def Minimax(state, depth, agent):
            """ Initially check the edje cases """
            if state.isLose() or state.isWin() or (depth == 0):
                return self.evaluationFunction(state), Directions.STOP

            """ Next, add the agents and check the state + action """
            nextAgent = (agent + 1) % totalAgents
            if agent == self.index:  # Max
                currentValue = float("-inf")
                currentAction = Directions.STOP
                actions = state.getLegalActions(agent)
                """ If the nextState is greater than currentState"""
                for action in actions:
                    state_reached = state.generateSuccessor(agent, action)
                    stateAction = Minimax(state_reached, depth - 1, nextAgent)
                    #print(stateAction)

                    if stateAction[0] > currentValue:
                        currentValue = stateAction[0]
                        currentAction = action
                    valueActionMax = (currentValue, currentAction)
                return valueActionMax

            else:  # Min
                currentValue = float("inf")
                currentAction = Directions.STOP
                actions = state.getLegalActions(agent)

                """ If the nextState is greater than currentState"""
                for action in actions:
                    state_reached = state.generateSuccessor(agent, action)
                    stateAction = Minimax(state_reached, depth - 1, nextAgent)
                    # print(stateAction)

                    if stateAction[0] < currentValue:
                        currentValue = stateAction[0]
                        currentAction = action
                    valueActionMin = (currentValue, currentAction)
                return valueActionMin

        totalAgents = gameState.getNumAgents()

        """ Iterate through the complete length and breath """
        currentValueAction = Minimax(gameState, self.depth * totalAgents, self.index)

        """" Return only action; because we will be getting a tuple of two values (currentValue, currentAction) """
        return currentValueAction[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    "*** YOUR CODE HERE ***"

    def getAction(self, gameState):

        def alphaBetaPruning(state, depth, alpha, beta, agent):
            # Note from Q3 that:
            # alpha is Max's best option on path to root
            # beta is Min's best option on path to root

            """ Initially check the edje cases """
            if state.isLose() or state.isWin() or (depth == 0):
                return self.evaluationFunction(state), Directions.STOP

            """ Next, add the agents and check the state + action """
            nextAgent = (agent + 1) % totalAgents
            if agent == self.index:  # Max
                currentValue = float("-inf")
                currentAction = Directions.STOP
                actions = state.getLegalActions(agent)
                """ If the nextState is greater than currentState """
                for action in actions:
                    state_reached = state.generateSuccessor(agent, action)
                    stateAction = alphaBetaPruning(state_reached, depth - 1, alpha, beta, nextAgent)
                    # print(stateAction)

                    if stateAction[0] > currentValue:
                        currentValue = stateAction[0]
                        currentAction = action
                    valueActionMax = (currentValue, currentAction)

                    """ Check the condition of alphaBeta pruning; when (currentValue > beta) return the tuple """
                    if currentValue > beta:
                        return valueActionMax
                    alpha = max(alpha, currentValue)

                return valueActionMax

            else:  # Min
                currentValue = float("inf")
                currentAction = Directions.STOP
                actions = state.getLegalActions(agent)

                """ If the nextState is greater than currentState"""
                for action in actions:
                    state_reached = state.generateSuccessor(agent, action)
                    stateAction = alphaBetaPruning(state_reached, depth - 1, alpha, beta, nextAgent)
                    # print(stateAction)

                    if stateAction[0] < currentValue:
                        currentValue = stateAction[0]
                        currentAction = action
                    valueActionMin = (currentValue, currentAction)

                    """ Check the condition of alphaBeta pruning; prune the part when (currentValue < alpha) statisfies """
                    if currentValue < alpha:
                        break
                    beta = min(beta, currentValue)

                return valueActionMin

        totalAgents = gameState.getNumAgents()

        """ Iterate through the complete length and breath """
        currentValueAction = alphaBetaPruning(gameState, self.depth * totalAgents, float("-inf"), float("inf"), self.index)

        """" Return only action; because we will be getting a tuple of two values (currentValue, currentAction) """
        return currentValueAction[1]

        #util.raiseNotDefined()

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

        def expectiMax(state, depth, agent):
            """ Initially check the edje cases """
            if state.isLose() or state.isWin() or (depth == 0):
                return self.evaluationFunction(state), Directions.STOP

            """ Next, add the agents and check the state + action """
            nextAgent = (agent + 1) % totalAgents
            if agent == self.index:  # Max
                currentValue = float("-inf")
                currentAction = Directions.STOP
                actions = state.getLegalActions(agent)

                """ If the nextState is greater than currentState"""
                for action in actions:
                    state_reached = state.generateSuccessor(agent, action)
                    stateAction = expectiMax(state_reached, depth - 1, nextAgent)
                    #print(stateAction)

                    if stateAction[0] > currentValue:
                        currentValue = stateAction[0]
                        currentAction = action
                    valueActionMax = (currentValue, currentAction)
                return valueActionMax

            else:  # Chance
                currentValue = []
                currentAction = Directions.STOP
                actions = state.getLegalActions(agent)

                for action in actions:
                    state_reached = state.generateSuccessor(agent, action)
                    stateAction = expectiMax(state_reached, depth - 1, nextAgent)
                    # print(stateAction)
                    currentValue.append(stateAction[0])

                """ Apply the logic of Chance; take the average of the children nodes"""
                currentValue = sum(currentValue) / len(currentValue)
                valueActionChance = (currentValue, currentAction)
                return valueActionChance

        totalAgents = gameState.getNumAgents()

        """ Iterate through the complete length and breath """
        currentValueAction = expectiMax(gameState, self.depth * totalAgents, self.index)

        """" Return only action; because we will be getting a tuple of two values (currentValue, currentAction) """
        return currentValueAction[1]

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

