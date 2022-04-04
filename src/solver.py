import numpy as np
from heapq import heappush, heappop
import time

nodeCreated = 0 #count the number of node created

def read_matrix(filename): #read the matrix from the file
    with open(filename, 'r') as fp:
        lines = fp.readlines()
    lines = [line.strip() for line in lines]
    lines = [line.split(' ') for line in lines]
    lines = [[int(x) for x in line] for line in lines]
    return np.array(lines)

def randomize(): #function to randomize the puzzle
    puzzle = np.arange(1,17)
    puzzle = puzzle.reshape(4,4)
    puzzle = np.random.permutation(puzzle)
    return puzzle

def matrixToList(arr): #convert the matrix to list
    arr1=[]
    for y in arr:
        for x in y:
            arr1.append(x)
    return arr1

def sigmaKurang(arr, listKurang): #function to calculate sigma kurang
    arr1=matrixToList(arr)
    inv_count = 0
    for i in range(16):
        curr_count = 0;
        for j in range(i + 1,16):
            if (arr1[i] > arr1[j]):
                inv_count+=1
                curr_count+=1
        listKurang[arr1[i]] = curr_count
    return inv_count

def checkEmptyPosition(arr): #check if the empty position value is zero or one
    for i in range(4):
        for j in range(4):
            if (arr[i][j] == 16):
                return int((i%2 == 0 and j%2 == 1) or (i%2 == 1 and j%2 == 0))

def sigmaKurangIPlusX(sigmakurang, X): #function to calculate sigma kurang[I] + X
    return (sigmakurang + X)
    
def isPossible(sigmakurang, X): #check if the puzzle is possible to solve
    return (sigmakurang + X) % 2 == 0

def calculateCost(mat, final): #function to calculate the estimation step taken
    count = 0
    for i in range(4):
        for j in range(4):
            if (mat[i][j] != final[i][j] and mat[i][j] != 16):
                count += 1         
    return count

def printMatrix(result): #print the matrix
    for row in range(4):
        for col in range(4):
            if result[row][col] == 16:
                if col == 3:
                    print("-", end="\n")
                else:
                    print("-", end="\t")
            else:
                if col == 3:
                    print(result[row][col], end="\n")
                else:
                    print(result[row][col], end="\t")
    print()

def getEmptyPosition(mat): #function to get the empty position
    for i in range(4):
        for j in range(4):
            if (mat[i][j] == 16):
                return (i,j)

def printPath(root): #function to print the path from initial puzzle to final puzzle
     
    if root.parent == None:
        return
     
    printPath(root.parent)
    printMove(root.move)
    printMatrix(root.mat)
    print()

def copyMatrix(mat): #function to copy the matrix
    newList = [[0 for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            newList[i][j] = mat[i][j]
    return newList

def isIdxValid(X, Y): #check if the index is valid
    return X >= 0 and X < 4 and Y >= 0 and Y < 4

class node: #class for node, used to generate solution tree
    def __init__(self, parent, mat, emptyPos, cost, level, move):
        self.parent = parent
        self.mat = mat
        self.emptyPos = emptyPos
        self.cost = cost
        self.level = level
        self.move = move
 
    def __lt__(self, nxt): #compare the node based on the cost, so the prioqueue will be sorted based on cost
        return self.cost < nxt.cost

class priorityQueue: #class for priority queue
    def __init__(self):
        self.heap = []
 
    def push(self, k):
        heappush(self.heap, k)
 
    def pop(self):
        return heappop(self.heap)
 
    def isEmpty(self):
        if not self.heap:
            return True
        else:
            return False

def createNode(mat, emptyPos, emptyPosAfter, level, parent, final, move):
    #function to create a node while moving
    global nodeCreated
    nodeCreated += 1
    newMatrix = copyMatrix(mat)
    x1 = emptyPos[0]
    y1 = emptyPos[1]
    x2 = emptyPosAfter[0]
    y2 = emptyPosAfter[1]
    newMatrix[x1][y1], newMatrix[x2][y2] = newMatrix[x2][y2], newMatrix[x1][y1] #swap the empty position with the new position
    newlevel = level + 1
    newcost = calculateCost(newMatrix, final) + newlevel #cost is cost of the new matrix + level
    newNode = node(parent, newMatrix, emptyPosAfter, newcost, newlevel, move)
    return newNode

def move(x): #function to move the empty position, will be added when the empty position is moved
    if (x == 0):
        return (-1,0)
    elif (x == 1):
        return (0,-1)
    elif (x == 2):
        return (1,0)
    elif (x == 3):
        return (0,1)

def printMove(x):
    #defined in the order of move (0 = up, 1 = left, 2 = down, 3 = right)
    if (x == None):
        print("Initial Matrix")
    elif (x == 0):
        print("Up")
    elif (x == 1):
        print("Left")
    elif (x == 2):
        print("Down")
    elif (x == 3):
        print("Right")

def solve(mat, final):
    emptyPos = getEmptyPosition(mat)
    pq = priorityQueue()
    start = time.time()
    if isPossible(sigmaKurang(mat, [0]*17), checkEmptyPosition(mat)):
        pq.push(node(None, mat, emptyPos, calculateCost(mat, final), 0, None)) #initial node
        while not pq.isEmpty():
            leastCost = pq.pop();  #pop the node with the least cost
            if (leastCost.cost == 0 or leastCost.cost == leastCost.level): #if the cost estimation is zero, the puzzle is solved
                stop = time.time()
                print("Solution found\n")
                print("Total number of nodes created: " + str(nodeCreated))
                print("Step by step solution: \n")
                printPath(leastCost)
                print("Total time taken: " + str(stop - start))
                return
            else:
                #check if the empty position can be moved in the direction of i
                #if the empty position can be moved, create a new node
                #in order to minimize step taken to solve the puzzle
                #program will not do any repetition move, such as move up then move down
                for i in range(4):
                    if leastCost.move == None or leastCost.move == i:
                        emptyPosChild = leastCost.emptyPos[0] + move(i)[0], leastCost.emptyPos[1] + move(i)[1]
                        if isIdxValid(emptyPosChild[0], emptyPosChild[1]):
                            pq.push(createNode(leastCost.mat, leastCost.emptyPos, emptyPosChild, leastCost.level, leastCost, final, i))
                    else:
                        currmove = i%2 #since the move is in the order of up, left, down, right, the move is categorized (by modulo 2) either 0 or 1
                        parentmove = leastCost.move % 2 #if the modulo result is the same, the move is repetition
                        if (currmove != parentmove):
                            emptyPosChild = leastCost.emptyPos[0] + move(i)[0], leastCost.emptyPos[1] + move(i)[1]
                            if isIdxValid(emptyPosChild[0], emptyPosChild[1]):
                                pq.push(createNode(leastCost.mat, leastCost.emptyPos, emptyPosChild, leastCost.level, leastCost, final, i))

                    
    else:
        print("No Possible Solution")