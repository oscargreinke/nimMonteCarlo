import time
import math
import random

currentNode = None
playerTurn = None

def flipTurns(state):
    turn = state[1]
    if turn == 1: 
        turn += 1 
        return (state[0], turn)
    elif turn == 2:
        turn -= 1 
        return (state[0], turn)
    else:
        print("Error: Invalid turn number")
        return -1

def isTerminal(state):
    if state[0] == []:
        return True
    else:
        for element in state[0]:
            if element == 0:
                pass
            elif element < 0:
                element = 0
            else:
                return False
        return True

def pruneState(state):
    for index, pile in enumerate(state[0]):
        if pile == 0:
            del(state[0][index])
    return state

def nextStates(state):
    states = []
    for index, st in enumerate(state[0]):
        if st >= 1:
            tempState = state[0][:]
            del(tempState[index])
            states.append(((tempState[:index] + [st-1]+ tempState[index:]),state[1]))
        if st >= 2:
            tempState = state[0][:]
            del(tempState[index])
            states.append(((tempState[:index] + [st-2]+ tempState[index:]), state[1]))
        if st >= 3:
            tempState = state[0][:]
            del(tempState[index])
            states.append(((tempState[:index] + [st-3]+ tempState[index:]),state[1]))
    return states

def setupGame():
    global currentNode, playerTurn
    pile = []
    numPiles = int(input("How many piles? "))
    maxPile = int(input("Maximum number of sticks? "))
    for i in range(0, numPiles):
        pile.append(random.randint(1, maxPile))
    first = input("Do you want to go first?(y/n) ")
    if first == 'y':
        playerTurn = 1
    elif first == 'n':
        playerTurn = 2
    else:
        print("Invalid choice - you're going first")
        playerFirst = 1
    state = (pile, playerTurn)
    currentNode = stateNode(state, None)
    print(state)
    return state

def playerMove(state):
    global currentNode
    piles = state[0]
    length = len(piles)
    pileNum = int(input("Which pile do you want to take from?(1-"+str(length)+") "))-1
    if piles[pileNum] < 3 and not piles[pileNum] == 0:
        amount = int(input("How many do you want to take?(1-"+str(piles[pileNum])+") "))
    else:
        amount = int(input("How many do you want to take?(1-3) "))
    piles[pileNum] -= amount
    st = flipTurns((piles, state[1]))
    st = pruneState(st)
    print(st)
    currentNode = stateNode(st, None)
    return st

def ucbi(node):
    global currentNode
    ucbVal = None
    if node.timesPlayed == 0:
        ucbVal = 2147483647
    else:
        avgVal = node.value/node.timesPlayed
        ucbVal = avgVal + 2*(math.sqrt(math.log(currentNode.timesPlayed)/node.timesPlayed))
    return ucbVal

def monteCarlo(node):
    global playerFirst
    curNode = node
    while(not curNode.children == []): #gets to leaf node
        ucbVal = -2147483647
        nextNode = curNode.children[0]
        for child in curNode.children:
            if ucbi(child) > ucbVal:
                ucbVal = ucbi(child)
                nextNode = child
        curNode = nextNode
    if curNode.timesPlayed == 0: #Now that we have a leaf node, check if visited
        gameVal = rollout(curNode.state) #not visited - rollout, backprop
        curNode.backPropagate(gameVal)
    else: # Has been visited
        if isTerminal(curNode.state):
            if curNode.state[1] == playerTurn:
                curNode.backPropagate(-10)
            curNode.backPropagate(10)
        else:
            states = nextStates(curNode.state)
            for state in states: #Expand
                curNode.addChild(state)
            curNode = curNode.children[0] #take first child
            gameVal = rollout(curNode.state) #rollout on the first child
            curNode.backPropagate(gameVal)

def rollout(state):
    global playerTurn
    if isTerminal(state):
        if state[1] == playerTurn: #If it's the player's turn, basically
            return -1
        return 1
    states = nextStates(state)
    nextState = flipTurns(states[random.randint(0, len(states)-1)])
    return rollout(nextState)

def computerMove(state):
    global currentNode
    for i in range(0, 20000):
        monteCarlo(currentNode) #Do the monte carlo
        val = -2147483647
    nextNode = None
    print("---AI DEBUG VALUES---")
    for child in currentNode.children:
        print(child.state)
        print(child.value)
        print(child.timesPlayed)
        print(ucbi(child))
        print("---------------------")
        ucbVal = ucbi(child)
        if ucbVal > val: #find the best child
            val = ucbVal
            nextNode = child
    nextNode.state = pruneState(nextNode.state)
    print(nextNode.state)
    return nextNode.state #Return that sate

class stateNode():
    def __init__(self, state, parent):
        self.state = state
        self.timesPlayed = 0
        self.value = 0
        self.parent = parent
        self.children = []
        
    def addChild(self, state):
        node = stateNode(state, self)
        self.children.append(node)

    def backPropagate(self, val):
        self.value += val
        self.timesPlayed += 1
        if not self.parent is None:
            return self.parent.backPropagate(val)
        else:
            return

def playGame():
    global playerTurn, currentNode
    state = setupGame()
    if playerTurn == 1:
        while True:
            state = playerMove(state)
            if isTerminal(state):
                print("You win!")
                break
            state = computerMove(state)
            if isTerminal(state):
                print("You lose!")
                break
    else:
        while True:
            state = computerMove(state)
            if isTerminal(state):
                print("You lose!")
                break
            state = playerMove(state)
            if isTerminal(state):
                print("You win!")
                break
    






