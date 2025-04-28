from collections import deque
import json
from states import find_next_states
import time
from AIPlayer import *

def BFS(initialState, timeout=300):
    start_time = time.time()
    queue = deque([(Node(initialState), [], [])])  #Queue of (node, path)
    visited = set()

    while queue:
        currentNode, path, directions = queue.popleft()
        currentStateTuple = convert_to_tuple(currentNode.grid)

        elapsedTime = time.time() - start_time
        if elapsedTime > timeout:
            print(f"Breadth-First Search exceeded the time limit of {timeout} seconds.")
            return None, None

        if not currentNode.helmetPos:
            return path, directions

        if currentStateTuple in visited:
            continue
        visited.add(currentStateTuple)

        for nextState, direction in zip(*find_next_states(currentNode.grid)):
            queue.append((Node(nextState, parent=currentNode, direction=direction), path + [currentNode.grid], directions + [currentNode.direction]))

    return None, None


def main():
    times = [9999] * 35
    for levelNum in range(1, 36):
        if levelNum != -1:
            try:
                fload = open(f"Levels/Level{levelNum}.json", "r")
                level = json.load(fload)
            except:
                print(f"File Level{levelNum} not found. Continuing.")
                continue

            print(f"Level {levelNum}")

            startTime = time.time()  #Start the timer
            path, directions = BFS(level)
            endTime = time.time()  #End the timer
            elapsedTime = endTime - startTime  #Calculate elapsed time
            print(f"Execution time: {elapsedTime:.4f} seconds")  #Print the execution time

            if directions or path:
                print(f"Directions: {directions}")
                times[levelNum-1] = elapsedTime
            else:
                print("Failed to find a solution within the time limit.")
    print(times)

if __name__ == '__main__':
    main()