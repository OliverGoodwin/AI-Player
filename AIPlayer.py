import json
import copy
from states import find_next_states
import numpy as np
import time  # Importing time module

try:
    fload = open("saved_level.json", "r")
    level = json.load(fload)
except:
    level = [[1]]


def convert_to_tuple(obj):
    if isinstance(obj, np.ndarray):
        # Recursively convert each ndarray into a tuple
        return tuple(convert_to_tuple(x) for x in obj)
    elif isinstance(obj, list):
        # If the object is a list, convert each element into a tuple
        return tuple(convert_to_tuple(x) for x in obj)
    else:
        return obj  # Return the object as is (non-ndarray, non-list)


class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.parent = parent
        self.grid = state
        self.helmetPos = []
        self.playerPos = []
        for y in range(len(state)):
            for x in range(len(state[y])):
                if 0 in state[y][x]:
                    self.playerPos.append((y, x))
                    break
        for y in range(len(state)):
            for x in range(len(state[y])):
                if 2 in state[y][x]:
                    self.helmetPos.append((y, x))
        self.g = g  # Cost from start to this node
        self.h = h  # Heuristic cost to the goal
        self.f = g + h  # Total cost (f = g + h)

    def __lt__(self, other):
        return self.f < other.f  # Compare based on the f value


def heuristic(state):
    try:
        source = state.playerPos[0]
        if not find_next_states(state.grid):
            return float('inf')
    
        min_distance = float('inf')
        for dest in state.helmetPos:
            distance = (abs(source[0] - dest[0]) + abs(source[1] - dest[1]))
            if distance < min_distance:
                min_distance = distance

        return min_distance
    except:
        return float('inf')


def IDAStar(currentNode, limit, closedSet):
    if currentNode.f > limit:
        return currentNode.f

    if not currentNode.helmetPos:
        print("No more helmets")
        path = []
        while currentNode:
            path.append(currentNode.grid)
            currentNode = currentNode.parent
        return path[::-1]

    # Convert the grid into a fully hashable type
    stateGrid = np.asarray(currentNode.grid, dtype=object)
    
    # Apply conversion to tuples for each element in the grid (also flatten)
    stateKey = tuple(convert_to_tuple(row) for row in stateGrid)

    # Check and add to closedSet
    if stateKey in closedSet:
        return float('inf')
    closedSet.add(stateKey)

    minf = float('inf')
    for nextState in find_next_states(currentNode.grid):
        g = currentNode.g + 1  # Adjust as needed for actual cost
        h = heuristic(Node(nextState))
        neighbourNode = Node(nextState, parent=currentNode, g=g, h=h)
        result = IDAStar(neighbourNode, limit, closedSet)

        if isinstance(result, list):
            return result
        minf = min(minf, result)

    print(f"Explored states: {len(closedSet)}")
    return minf


def A_Star_Search(initialState):
    limit = heuristic(Node(initialState))
    while True:
        closedSet = set()
        result = IDAStar(Node(initialState), limit, closedSet)
        if isinstance(result, list):
            return result
        
        limit = result


def main():
    start_time = time.time()  # Start the timer
    
    path = A_Star_Search(level)
    print(path)

    with open("saved_level.json", "w") as f:
        json.dump(path[len(path) - 1], f)

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Execution time: {elapsed_time:.4f} seconds")  # Print the execution time


main()
