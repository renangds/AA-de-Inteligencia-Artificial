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

class GhostAgent(Agent):
    def __init__(self, index):
        self.index = index

    def getAction(self, state):
        problem = PositionSearchProblem(state) #Mapeia todos os estados do jogo
        problem.goal = state.getPacmanPosition() #Mapeia o estado atual do pacman
        problem.startState = state.getGhostPosition(self.index) #Mapeia o estado atual do objeto do fantasma

        pqueue = util.PriorityQueue() #Cria uma fila de prioridades
        current_state = [problem.getStartState(), [], 0] #Cria o estado inicial
        successors = None #Cria um estado sucessor vazio
        explored = set() #cria ums lista de nos expandidos
        item = None #Cria uma variavel para armazenar os dados de um estado
        explored.add(problem.getStartState()) #Insere o novo estado

        #Aqui e o algoritmo a star
        while not problem.isGoalState(current_state[0]):
            (current_pos, directions, cost) = current_state #Tupla do No atual
            successors = problem.getSuccessors(current_pos) #Usa a funcao getSucessors para gerar todos os estados sucessores
            for item in successors:
                ghostsPos = state.getGhostPositions() #Pega a posicao de todos os fantasmas
                ghostsPos.remove(state.getGhostPosition(self.index)) #Remove si mesmo pois somente o outro fantasma q nao pode
                if not item[0] in ghostsPos: #Se nao houver fantasmas no caminho, ele insere o no na fila
                    pqueue.push((item[0], directions + [item[1]], cost + item[2]),
                                cost + item[2] + util.manhattanDistance(item[0], problem.goal))
            while(True):
                if (pqueue.isEmpty()): #Se a fila estiver vazia, termina
                    return None
                item = pqueue.pop() #Retira o item com maior prioridade da lista
                if item[0] not in explored: #Se o no nao existir na lista de estados visitados, ele sai
                    break
            current_state = (item[0], item[1], item[2]) #Adiciona um novo estado caso contrario
            explored.add(item[0]) #adiciona a tupla com a posicao do no ja visitado
        return current_state[1][0] #retorna a acao

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
