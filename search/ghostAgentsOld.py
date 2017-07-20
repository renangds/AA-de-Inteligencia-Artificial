# ghostAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util
from searchAgents import PositionSearchProblem
from searchAgents import manhattanHeuristic

'''class newGhostAgent(Agent):
    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        estadosJogo = PositionSearchProblem(state) #Mapeia a posicao de todos os agentes
        pacman = state.getPacmanPosition() #Mapeia a posicao atual do pacman
        fantasma = state.getGhostPosition(self.index) #Mapeia a posicao DO FANTASMA desse objeto
        prioridade = util.PriorityQueue() #Cria uma heap para auxiliar na busca A star

        #closure para verificar o melhor caminho a ter tomado
        def BestChoice(pfan, ppac):
            no = manhattanDistance(pfan, ppac)

        while not prioridade.isEmpty():
            manhattanDistance
'''

class GhostAgent(Agent):
    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        problem = PositionSearchProblem(state) #Mapeia todos os estados do jogo
        problem.goal = state.getPacmanPosition() #Mapeia o estado atual do pacman
        problem.startState = state.getGhostPosition(self.index) #Mapeia o estado atual do objeto do fantasma

        frontier = util.PriorityQueue() #Cria uma fila de prioridade
        frontier.push(problem.getStartState(), manhattanHeuristic(problem.getStartState(), problem)) #coloca na heap o primeiro estado
        explored = [] #Nos expandidos
        paths = {} #Todos os estados que foram percorridos
        totalCost = {} #Custo total
        paths[problem.getStartState()]= list()
        totalCost[problem.getStartState()]=0

        def isBestCostforState(cost,state):
            for n in frontier.heap:
                if n[1] == state:
                    if (n[1] in totalCost.keys()) and (totalCost[n[1]]> cost):
                        frontier.heap.remove(n)
                        return True
                    else:
                        return False
            return True

        while not frontier.isEmpty():
            s = frontier.pop()
            if problem.isGoalState(s):
                return paths.popitem()[1][0]
            explored.append(s)
            successors = problem.getSuccessors(s)
            for successor in successors:
                successorState=successor[0]
                move=successor[1]
                cost=successor[2]
                if (successorState not in explored and isBestCostforState(totalCost[s]+cost,successorState)):
                    paths[successorState] = list(paths[s]) + [move]
                    totalCost[successorState] = totalCost[s] + cost
                    frontier.push(successorState, manhattanHeuristic(successorState, problem) + totalCost[successorState])
        return []

'''class GhostAgent( Agent ):
  def __init__( self, index ):
    self.index = index

  def getAction( self, state ):
    dist = self.getDistribution(state)
    if len(dist) == 0:
      return Directions.STOP
    else:
      return util.chooseFromDistribution( dist )

  def getDistribution(self, state):
    "Returns a Counter encoding a distribution over actions from the provided state."
    util.raiseNotDefined()
'''

class RandomGhost( GhostAgent ):
  "A ghost that chooses a legal action uniformly at random."
  def getDistribution( self, state ):
    dist = util.Counter()
    for a in state.getLegalActions( self.index ): dist[a] = 1.0
    dist.normalize()
    return dist

class DirectionalGhost( GhostAgent ):
  "A ghost that prefers to rush Pacman, or flee when scared."
  def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
    self.index = index
    self.prob_attack = prob_attack
    self.prob_scaredFlee = prob_scaredFlee

  def getDistribution( self, state ):
    # Read variables from state
    ghostState = state.getGhostState( self.index )
    legalActions = state.getLegalActions( self.index )
    pos = state.getGhostPosition( self.index )
    isScared = ghostState.scaredTimer > 0

    speed = 1
    if isScared: speed = 0.5

    actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
    newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
    pacmanPosition = state.getPacmanPosition()

    # Select best actions given the state
    distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
    if isScared:
      bestScore = max( distancesToPacman )
      bestProb = self.prob_scaredFlee
    else:
      bestScore = min( distancesToPacman )
      bestProb = self.prob_attack
    bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

    # Construct distribution
    dist = util.Counter()
    for a in bestActions: dist[a] = bestProb / len(bestActions)
    for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
    dist.normalize()
    return dist
