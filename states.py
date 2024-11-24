import json
import copy


try:
    fload = open("saved_level.json", "r")
    level = json.load(fload)
except:
    level = [[1]]


def find_next_states(initialState):
    #use deepcopy when resetting states to avoid variable in possible states list changing as well
    state = copy.deepcopy(initialState)

    possibleStates = []

    for row, y in enumerate(state):
        for col, list in enumerate(y):
            if 0 in list:
                johnnyPos = (row, col)
            
    #case 1: empty cell beneath Johnny. Next move will always be falling, unless on ladder
    if state[johnnyPos[0] + 1][johnnyPos[1]] == [-1] and 5 not in state[johnnyPos[0]][johnnyPos[1]]:
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        state[johnnyPos[0] + 1][johnnyPos[1]].append(0)
        return state
    
    #case 2: empty cell or ladder left or right. This move can be a next state, not necesarily the best move though
    #edge cases should not matter here because the level will always be surrounded by a layer of bricks, therefore, Johnny will not be at [0, x] or [y, 0]
    #right
    #if johnny is under a crate, the crate will fall after moving, unless on a ladder. The crate will always end up in Johnny's original position
    if state[johnnyPos[0]][johnnyPos[1] + 1] in ([-1], [-1, 5]):
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        state[johnnyPos[0]][johnnyPos[1] + 1].append(0)
        if 3 in state[johnnyPos[0] - 1][johnnyPos[1]] and 5 not in state[johnnyPos[0]][johnnyPos[1]]:
            state[johnnyPos[0]][johnnyPos[1]].append(3)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
    #left
    if state[johnnyPos[0]][johnnyPos[1] - 1] in ([-1], [-1, 5]):
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        state[johnnyPos[0]][johnnyPos[1] - 1].append(0)
        if 3 in state[johnnyPos[0] - 1][johnnyPos[1]] and 5 not in state[johnnyPos[0]][johnnyPos[1]]:
            state[johnnyPos[0]][johnnyPos[1]].append(3)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)

    #case 3: Johnny on ladder cell with ladder or empty space above and below
    #above
    if 5 in state[johnnyPos[0]][johnnyPos[1]]:
        if state[johnnyPos[0] - 1][johnnyPos[1]] in ([-1], [-1, 5]):
            state[johnnyPos[0]][johnnyPos[1]].remove(0)
            state[johnnyPos[0] - 1][johnnyPos[1]].append(0)
            possibleStates.append(state)
            state = copy.deepcopy(initialState)
        if state[johnnyPos[0] + 1][johnnyPos[1]] in ([-1], [-1, 5]):
            state[johnnyPos[0]][johnnyPos[1]].remove(0)
            state[johnnyPos[0] + 1][johnnyPos[1]].append(0)
            possibleStates.append(state)
            state = copy.deepcopy(initialState)
    
    #case 4: crate left or right. Nothing behing the crate. Johnny can push the crate
    #left
    if 3 in state[johnnyPos[0]][johnnyPos[1] - 1] and state[johnnyPos[0]][johnnyPos[1] - 2] == [-1]:
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        state[johnnyPos[0]][johnnyPos[1] - 1].append(0)
        state[johnnyPos[0]][johnnyPos[1] - 1].remove(3)
        #the crate can fall if pushed. It could also fall multiple cells
        i = 0
        canPlace = False
        while canPlace == False:
            if state[johnnyPos[0] + i + 1][johnnyPos[1] - 2] == [-1]:
                i += 1
            else:
                state[johnnyPos[0] + i][johnnyPos[1] - 2].append(3)
                canPlace = True
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
    #right
    if 3 in state[johnnyPos[0]][johnnyPos[1] + 1] and state[johnnyPos[0]][johnnyPos[1] + 2] == [-1]:
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        state[johnnyPos[0]][johnnyPos[1] + 1].append(0)
        state[johnnyPos[0]][johnnyPos[1] + 1].remove(3)
        #the crate can fall if pushed. It could also fall multiple cells
        i = 0
        canPlace = False
        while canPlace == False:
            if state[johnnyPos[0] + i + 1][johnnyPos[1] + 2] == [-1]:
                i += 1
            else:
                state[johnnyPos[0] + i][johnnyPos[1] + 2].append(3)
                canPlace = True
        possibleStates.append(state)
        state = copy.deepcopy(initialState)

    #case 5: water or helmet left or right. Johnny removes the water or helmet.
    #left
    if 4 in state[johnnyPos[0]][johnnyPos[1] - 1]or 2 in state[johnnyPos[0]][johnnyPos[1] - 1]:
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        state[johnnyPos[0]][johnnyPos[1] - 1].append(0)
        if 4 in state[johnnyPos[0]][johnnyPos[1] - 1]:
            state[johnnyPos[0]][johnnyPos[1] - 1].remove(4)
        elif 2 in state[johnnyPos[0]][johnnyPos[1] - 1]:
            state[johnnyPos[0]][johnnyPos[1] - 1].remove(2)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
    #right
    if 4 in state[johnnyPos[0]][johnnyPos[1] + 1] or 2 in state[johnnyPos[0]][johnnyPos[1] + 1]:
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        state[johnnyPos[0]][johnnyPos[1] + 1].append(0)
        if 4 in state[johnnyPos[0]][johnnyPos[1] + 1]:
            state[johnnyPos[0]][johnnyPos[1] + 1].remove(4)
        elif 2 in state[johnnyPos[0]][johnnyPos[1] + 1]:
            state[johnnyPos[0]][johnnyPos[1] + 1].remove(2)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
                
    return possibleStates


def main():
    nextStates = find_next_states(level)

    for num, i in enumerate(nextStates):
        print(num)
        print(str(i) + "\n")

    
    #use if wanting to test a current state's outcomes
    #with open("saved_level.json", "w") as f:
        #json.dump(nextStates[0], f) #change 0 with number of state you want to visit

main()