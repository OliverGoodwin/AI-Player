import json
from states import find_next_states
import time
from AIPlayer import *

def DFS(initialState, timeout=300):
    start_time = time.time()
    stack = [(Node(initialState), [], [])]  #Stack of (node, path)
    visited = set()

    while stack:
        currentNode, path, directions = stack.pop()
        currentStateTuple = convert_to_tuple(currentNode.grid)

        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            print(f"Depth-First Search exceeded the time limit of {timeout} seconds.")
            return None, None, None

        if not currentNode.helmetPos:
            return path, directions, len(visited)

        if currentStateTuple in visited:
            continue

        visited.add(currentStateTuple)

        for next_state, direction in zip(*find_next_states(currentNode.grid)):
            stack.append((Node(next_state, parent=currentNode, direction=direction), path + [currentNode.grid], directions + [currentNode.direction]))

    return None, None, None


def main():
    times = [9999] * 50
    lengths = [9999] * 50
    size = [9999] * 50
    for levelNum in range(50, 51):
        if levelNum != -1:
            try:
                fload = open(f"Levels/Level{levelNum}.json", "r")
                level = json.load(fload)
            except:
                print(f"File Level{levelNum} not found. Continuing.")
                continue

            print(f"Level {levelNum}")

            startTime = time.time()  #Start the timer
            path, directions, visited = DFS(level)
            endTime = time.time()  #End the timer
            elapsedTime = endTime - startTime  #Calculate elapsed time
            print(f"Execution time: {elapsedTime:.4f} seconds")  #Print the execution time
            if directions or path:
                print(f"Path length: {len(path)}")
                print(f"Nodes explored: {visited}")
                print(f"Directions: {directions}")
                times[levelNum-1] = elapsedTime
                lengths[levelNum-1] = len(path)
                size[levelNum-1] = visited
            else:
                print("Failed to find a solution within the time limit.")
    print(times)
    print(lengths)
    print(size)

if __name__ == '__main__':
    main()