# pacmanAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from pacman import Directions
from game import Agent
import random
import game
import util
from searchAgents import PositionSearchProblem
from searchAgents import manhattanHeuristic

class PacmanAgent(game.Agent):
    def getAction(self, state):
        problem = PositionSearchProblem(state) #Mapeia todos os estados do jogo
        problem.startState = state.getPacmanPosition() #Mapeia o estado atual do objeto do pacman

        allFoods = list(state.getFood().asList()) #Insere uma lista com todas as comidas

        x, food = min([(util.manhattanDistance(problem.getStartState(), food), food) for food in
		                     allFoods]) #Heuristica da comida

        problem.goal = food #Objetivo

        pqueue = util.PriorityQueue() #Cria uma heap
        current_state = [problem.getStartState(), [], 0] #Estado atual
        successors = None #Cria um estado sucessor vazio
        explored = set() #cria ums lista de nos expandidos
        item = None #Cria uma variavel para armazenar os dados de um estado
        explored.add(problem.getStartState()) #Insere o novo estado

        #Aqui e o algoritmo a star
        while not problem.isGoalState(current_state[0]):
            (current_pos, directions, cost) = current_state #Tupla do No atual
            successors = problem.getSuccessors(current_pos) #Usa a funcao getSucessors para gerar todos os estados sucessores
            for item in successors:
                if not item[0] in state.getGhostPositions(): #Se existir fantasma no caminho do pacman, ele nao expande
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

class LeftTurnAgent(game.Agent):
  "An agent that turns left at every opportunity"

  def getAction(self, state):
    legal = state.getLegalPacmanActions()
    current = state.getPacmanState().configuration.direction
    if current == Directions.STOP: current = Directions.NORTH
    left = Directions.LEFT[current]
    if left in legal: return left
    if current in legal: return current
    if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
    if Directions.LEFT[left] in legal: return Directions.LEFT[left]
    return Directions.STOP

class GreedyAgent(Agent):
  def __init__(self, evalFn="scoreEvaluation"):
    self.evaluationFunction = util.lookup(evalFn, globals())
    assert self.evaluationFunction != None

  def getAction(self, state):
    # Generate candidate actions
    legal = state.getLegalPacmanActions()
    if Directions.STOP in legal: legal.remove(Directions.STOP)

    successors = [(state.generateSuccessor(0, action), action) for action in legal]
    scored = [(self.evaluationFunction(state), action) for state, action in successors]
    bestScore = max(scored)[0]
    bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
    return random.choice(bestActions)

def scoreEvaluation(state):
  return state.getScore()
