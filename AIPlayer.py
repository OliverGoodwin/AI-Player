import json
import heapq
from states import find_next_states

try:
    fload = open("saved_level.json", "r")
    level = json.load(fload)
except:
    level = [[1]]


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
        dest = state.helmetPos[0]
    except:
        return float('inf')
    
    if not find_next_states(state.grid):
        return float('inf')
    return min(abs(source[0] - dest[0]) + abs(source[1] - dest[1]) for dest in state.helmetPos)

def A_Star_Search(initialState):
    openList = []
    closedList = []

    startNode = Node(initialState)
    heapq.heappush(openList, startNode)

    while openList:
        
        currentNode = heapq.heappop(openList)

        if not currentNode.helmetPos:
            print("No more helmets")
            path = []
            while currentNode:
                path.append(currentNode.grid)
                currentNode = currentNode.parent
            return path[::-1]
        
        closedList.append(currentNode.grid)

        #Cost is always 1 as of now, change to cost when adding macro moves
        for nextState in find_next_states(currentNode.grid):
            if nextState in closedList:
                continue
            
            g = currentNode.g + 1#Change this to cost when adding macro moves
            h = heuristic(Node(nextState))
            neighbourNode = Node(nextState, parent=currentNode, g=g, h=h)
            
            heapq.heappush(openList, neighbourNode)

    return None


def main():
    path = A_Star_Search(level)
    print(path)

    with open("saved_level.json", "w") as f:
        json.dump(path[len(path) - 1], f)
    
main()