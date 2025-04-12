import json
from states import find_next_states
import numpy as np
import time
from python_tsp.exact import solve_tsp_dynamic_programming


try:
    fload = open("saved_level.json", "r")
    level = json.load(fload)
except:
    level = [[1]]


def convert_to_tuple(obj):
    if isinstance(obj, np.ndarray) or isinstance(obj, list):
        #Recursively convert each array and list into a tuple
        return tuple(convert_to_tuple(x) for x in obj)
    else:
        return obj  #Return the object as is (non-array, non-list)


class Node:
    def __init__(self, state, parent=None, direction="start", g=0, h=0):
        self.parent = parent
        self.grid = state
        self.direction = direction
        self.helmetPos = []
        self.playerPos = []
        for y in range(len(state)):
            for x in range(len(state[y])):
                if 0 in state[y][x]:
                    self.playerPos.append((y, x))
                    break
        for y in range(len(state)):
            for x in range(len(state[y])):
                if 2 in state[y][x] or 7 in state[y][x]:
                    self.helmetPos.append((y, x))

        self.distanceMatrix = self.create_distance_matrix()

        self.g = g  #Cost from start to this node
        self.h = h  #Heuristic cost to the goal
        self.f = g + h  #Total cost (f = g + h)

    def __lt__(self, other):
        return self.f < other.f  # Compare based on the f value
    
    def manhattan_distance(self, pos1, pos2):
        return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])
    
    def create_distance_matrix(self):
        positions = self.playerPos + self.helmetPos
        n = len(positions)
        distMatrix = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(1, n): #Start at 1 to make distance from helmet to player 0
                if i != j:
                    distMatrix[i][j] = self.manhattan_distance(positions[i], positions[j])

        return distMatrix


def heuristic(state):
    try:
        """source = state.playerPos[0]
        if not find_next_states(state.grid):
            return float('inf')
    
        minDistance = float('inf')
        for dest in state.helmetPos:
            distance = (abs(source[0] - dest[0]) + abs(source[1] - dest[1]))
            if distance < minDistance:
                minDistance = distance

        return minDistance"""

        #Use python_tsp library to solve Travelling Salesperson Problem
        #print(state.distanceMatrix)
        distMatrix = np.array(state.distanceMatrix)
        tspPath, distance = solve_tsp_dynamic_programming(distMatrix)
        return distance

    except:
        return float('inf')


def IDAStar(currentNode, limit, closedSet):
    if currentNode.f > limit:
        return currentNode.f

    if not currentNode.helmetPos:
        #print("No more helmets")
        path = []
        directions = []
        while currentNode:
            path.append(currentNode.grid)
            directions.append(currentNode.direction)
            currentNode = currentNode.parent
        return path[::-1], directions[::-1]

    #Convert the grid into a fully hashable type
    stateGrid = np.asarray(currentNode.grid, dtype=object)
    
    #Apply conversion to tuples for each element in the grid (also flatten)
    stateKey = tuple(convert_to_tuple(row) for row in stateGrid)

    #Check and add to closedSet
    if stateKey in closedSet:
        return float('inf')
    closedSet.add(stateKey)

    minf = float('inf')
    for nextState, direction in zip(*find_next_states(currentNode.grid)):
        g = currentNode.g + 1  #Adjust as needed for actual cost
        h = heuristic(Node(nextState))
        neighbourNode = Node(nextState, parent=currentNode, direction=direction, g=g, h=h)
        result = IDAStar(neighbourNode, limit, closedSet)
        if isinstance(result, tuple):
            path, directions = result
            return path, directions
        minf = min(minf, result)

    #print(f"Explored states: {len(closedSet)}")
    return minf


def A_Star_Search(initialState):
    limit = heuristic(Node(initialState))
    #print(limit)
    while True:
        closedSet = set()
        result = IDAStar(Node(initialState), limit, closedSet)
        if isinstance(result, tuple):
            path, directions = result
            return path, directions
        
        limit = result


def main():
    for levelNum in range(1, 10):
        try:
            fload = open(f"Levels/Level{levelNum}.json", "r")
            level = json.load(fload)
        except:
            print(f"File Level{levelNum} not found. Continuing.")
            continue

        print(f"Level {levelNum}")

        startTime = time.time()  #Start the timer
        path, directions = A_Star_Search(level)
        endTime = time.time()  #End the timer
        elapsedTime = endTime - startTime  #Calculate elapsed time
        print(f"Execution time: {elapsedTime:.4f} seconds")  #Print the execution time
        print(f"Directions: {directions}")

main()
