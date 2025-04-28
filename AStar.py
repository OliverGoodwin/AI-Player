import json
import heapq
from states import find_next_states
from AIPlayer import *

def A_Star(initialState, timeout = 300):
    frontier= []
    closedList = set()
    startTime=time.time()
    elapsedTime = 0

    startNode = Node(initialState)
    heapq.heappush(frontier, startNode)

    while frontier and elapsedTime < timeout:
        elapsedTime = time.time() - startTime
        currentNode = heapq.heappop(frontier)

        if not currentNode.helmetPos:
            path = []
            directions = []
            while currentNode:
                path.append(currentNode.grid)
                directions.append(currentNode.direction)
                currentNode = currentNode.parent
            return path[::-1], directions[::-1], len(closedList)
        
        #Convert the grid into a fully hashable type
        stateGrid = np.asarray(currentNode.grid, dtype=object)
    
        #Apply conversion to tuples for each element in the grid (also flatten)
        stateKey = tuple(convert_to_tuple(row) for row in stateGrid)

        closedList.add(stateKey)

        #Cost is always 1 as of now, change to cost when adding macro moves
        for nextState, direction in zip(*find_next_states(currentNode.grid)):
            if tuple(convert_to_tuple(row) for row in nextState) in closedList:
                continue
            g = currentNode.g + 1  #Adjust as needed for actual cost
            h = heuristic(Node(nextState))
            neighbourNode = Node(nextState, parent=currentNode, direction=direction, g=g, h=h)
            
            heapq.heappush(frontier, neighbourNode)

    return None, None, None


def main():
    times = [9999] * 50
    lengths = [9999] * 50
    size = [9999] * 50
    directionsArray = [None] * 50
    for levelNum in range(1, 51):
        if levelNum != -1:
            try:
                fload = open(f"Levels/Level{levelNum}.json", "r")
                level = json.load(fload)
            except:
                print(f"File Level{levelNum} not found. Continuing.")
                continue

            print(f"Level {levelNum}")

            startTime = time.time()  #Start the timer
            global levelNode
            levelNode = Node(level)
            path, directions, visited = A_Star(level)
            endTime = time.time()  #End the timer
            elapsedTime = endTime - startTime  #Calculate elapsed time
            print(f"Execution time: {elapsedTime:.4f} seconds")  #Print the execution time

            if directions or path:
                print(f"Path length: {len(path)}")
                print(f"Nodes explored: {visited}")
                print(f"Directions: {directions}")
                times[levelNum-1] = elapsedTime
                lengths[levelNum-1] = len(path)
                directionsArray[levelNum-1] = directions
            else:
                print("Failed to find a solution within the time limit.")
            
    print(times)
    print(lengths)
    print(directionsArray)


if __name__ == '__main__':
    main()