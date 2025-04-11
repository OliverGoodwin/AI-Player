import json
import copy


def find_next_states(initialState):
    #use deepcopy when resetting states to avoid variable in possible states list changing as well
    state = copy.deepcopy(initialState)

    possibleStates = []

    for row, y in enumerate(state):
        for col, list in enumerate(y):
            if 0 in list:
                johnnyPos = (row, col)
            
    #case 1: empty cell beneath Johnny, on roof or ladder.
    if state[johnnyPos[0] + 1][johnnyPos[1]] == [-1] and (6 in state[johnnyPos[0]][johnnyPos[1]] or 5 in state[johnnyPos[0]][johnnyPos[1]]):
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        i = 0
        canPlace = False
        while canPlace == False:
            if state[johnnyPos[0] + i + 1][johnnyPos[1]] == [-1]:
                i += 1
            else:
                state[johnnyPos[0] + i][johnnyPos[1]].append(0)
                canPlace = True
        state = fallingTilesTest(state)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
        #print("case 1")
    
    #case 2: empty cell or ladder or roof left or right. This move can be a next state, not necesarily the best move though
    #edge cases should not matter here because the level will always be surrounded by a layer of bricks, therefore, Johnny will not be at [0, x] or [y, 0]
    #johnny can fall if no block underneath left or right
    #if johnny is under a crate or helmet, the crate will fall after moving, unless on a ladder. The crate will always end up in Johnny's original position
    #right
    if state[johnnyPos[0]][johnnyPos[1] + 1] in ([-1], [-1, 5], [-1, 6]):
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        #Crate above Johnny
        if 3 in state[johnnyPos[0] - 1][johnnyPos[1]] and 5 not in state[johnnyPos[0]][johnnyPos[1]] and 6 not in state[johnnyPos[0]][johnnyPos[1]]:
            state[johnnyPos[0]][johnnyPos[1]].append(3)
            state[johnnyPos[0] - 1][johnnyPos[1]].remove(3)
        #Helmet above Johnny
        if 2 in state[johnnyPos[0] - 1][johnnyPos[1]] and 5 not in state[johnnyPos[0]][johnnyPos[1]] and 6 not in state[johnnyPos[0]][johnnyPos[1]]:
            state[johnnyPos[0]][johnnyPos[1]].append(2)
            state[johnnyPos[0] - 1][johnnyPos[1]].remove(2)
        if 5 not in state[johnnyPos[0]][johnnyPos[1] + 1] and 6 not in state[johnnyPos[0]][johnnyPos[1] + 1]:
            i = 0
            canPlace = False
            while canPlace == False:
                if state[johnnyPos[0] + i + 1][johnnyPos[1] + 1] == [-1]:
                    i += 1
                else:
                    state[johnnyPos[0] + i][johnnyPos[1] + 1].append(0)
                    canPlace = True
        else:
            state[johnnyPos[0]][johnnyPos[1] + 1].append(0)
        state = fallingTilesTest(state)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
        #print("case 2")
    #left
    if state[johnnyPos[0]][johnnyPos[1] - 1] in ([-1], [-1, 5], [-1, 6]):
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        #Crate above Johnny
        if 3 in state[johnnyPos[0] - 1][johnnyPos[1]] and 5 not in state[johnnyPos[0]][johnnyPos[1]] and 6 not in state[johnnyPos[0]][johnnyPos[1]]:
            state[johnnyPos[0]][johnnyPos[1]].append(3)
            state[johnnyPos[0] - 1][johnnyPos[1]].remove(3)
        #Helmet above Johnny
        if 2 in state[johnnyPos[0] - 1][johnnyPos[1]] and 5 not in state[johnnyPos[0]][johnnyPos[1]] and 6 not in state[johnnyPos[0]][johnnyPos[1]]:
            state[johnnyPos[0]][johnnyPos[1]].append(2)
            state[johnnyPos[0] - 1][johnnyPos[1]].remove(2)
        if 5 not in state[johnnyPos[0]][johnnyPos[1] - 1] and 6 not in state[johnnyPos[0]][johnnyPos[1] - 1]:
            i = 0
            canPlace = False
            while canPlace == False:
                if state[johnnyPos[0] + i + 1][johnnyPos[1] - 1] == [-1]:
                    i += 1
                else:
                    state[johnnyPos[0] + i][johnnyPos[1] - 1].append(0)
                    canPlace = True
        else:
            state[johnnyPos[0]][johnnyPos[1] - 1].append(0)
        state = fallingTilesTest(state)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
        #print("case 2")

    #case 3: Johnny on ladder or roof with ladder or empty space or roof above and below
    #above
    if 5 in state[johnnyPos[0]][johnnyPos[1]] or 6 in state[johnnyPos[0]][johnnyPos[1]]:
        if state[johnnyPos[0] - 1][johnnyPos[1]] in ([-1], [-1, 5], [-1, 6]):
            state[johnnyPos[0]][johnnyPos[1]].remove(0)
            state[johnnyPos[0] - 1][johnnyPos[1]].append(0)
            state = fallingTilesTest(state)
            possibleStates.append(state)
            state = copy.deepcopy(initialState)
            #print("case 3")
        if state[johnnyPos[0] + 1][johnnyPos[1]] in ([-1, 5], [-1, 6]):
            state[johnnyPos[0]][johnnyPos[1]].remove(0)
            state[johnnyPos[0] + 1][johnnyPos[1]].append(0)
            state = fallingTilesTest(state)
            possibleStates.append(state)
            state = copy.deepcopy(initialState)
            #print("case 3")
    
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
        state = fallingTilesTest(state)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
        #print("case 4")
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
        state = fallingTilesTest(state)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
        #print("case 4")

    #case 5: water or helmet or still helmet left or right. Johnny removes the water or helmet.
    #left
    if 4 in state[johnnyPos[0]][johnnyPos[1] - 1] or 2 in state[johnnyPos[0]][johnnyPos[1] - 1] or 7 in state[johnnyPos[0]][johnnyPos[1] - 1]:
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        state[johnnyPos[0]][johnnyPos[1] - 1].append(0)
        if 4 in state[johnnyPos[0]][johnnyPos[1] - 1]:
            state[johnnyPos[0]][johnnyPos[1] - 1].remove(4)
        elif 2 in state[johnnyPos[0]][johnnyPos[1] - 1]:
            state[johnnyPos[0]][johnnyPos[1] - 1].remove(2)
        elif 7 in state[johnnyPos[0]][johnnyPos[1] - 1]:
            state[johnnyPos[0]][johnnyPos[1] - 1].remove(7)
        state = fallingTilesTest(state)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
        #print("case 5")
    #right
    if 4 in state[johnnyPos[0]][johnnyPos[1] + 1] or 2 in state[johnnyPos[0]][johnnyPos[1] + 1] or 7 in state[johnnyPos[0]][johnnyPos[1] + 1]:
        state[johnnyPos[0]][johnnyPos[1]].remove(0)
        state[johnnyPos[0]][johnnyPos[1] + 1].append(0)
        if 4 in state[johnnyPos[0]][johnnyPos[1] + 1]:
            state[johnnyPos[0]][johnnyPos[1] + 1].remove(4)
        elif 2 in state[johnnyPos[0]][johnnyPos[1] + 1]:
            state[johnnyPos[0]][johnnyPos[1] + 1].remove(2)
        elif 7 in state[johnnyPos[0]][johnnyPos[1] + 1]:
            state[johnnyPos[0]][johnnyPos[1] + 1].remove(7)
        state = fallingTilesTest(state)
        possibleStates.append(state)
        state = copy.deepcopy(initialState)
        #print("case 5")

    #case 6: Johnny in empty tile. Ladder or roof under Johnny. Can climb down ladder
    if state[johnnyPos[0]][johnnyPos[1]] in [[-1, 0], [0, -1]]:
        if 5 in state[johnnyPos[0] + 1][johnnyPos[1]] or 6 in state[johnnyPos[0] + 1][johnnyPos[1]]:
            state[johnnyPos[0]][johnnyPos[1]].remove(0)
            state[johnnyPos[0] + 1][johnnyPos[1]].append(0)
            state = fallingTilesTest(state)
            possibleStates.append(state)
            state = copy.deepcopy(initialState)
            #print("case 6")
                
    return possibleStates


#If anything is still floating after this, loop throught the level until nothing is floating.
#This could cause the computational power to become large, maybe try to do this in the cases later.
#Start from the bottom and work up, as an item could fall which could make another item fall.
def fallingTilesTest(state):
    for y in range(len(state) - 1, -1, -1):  # Start from the last row
        for x in range(len(state[y])):
            if state[y][x] in [[-1, 2], [-1, 3], [-1, 0]]:
                tile = state[y][x][1]  # Extract the tile type (2 or 3)
                
                i = 1  # Start checking one row below
                while y + i < len(state) and state[y + i][x] == [-1]:  # Check bounds and empty space
                    i += 1
                
                # Place the tile in the row above the first non-empty space
                state[y + i - 1][x].append(tile)
                state[y][x].remove(tile)
    return state

"""def main():
    try:
        fload = open("saved_level.json", "r")
        level = json.load(fload)
    except:
        level = [[1]]

    nextStates = find_next_states(level)

    for num, i in enumerate(nextStates):
        print(num)
        print(str(i) + "\n")

    
    #use if wanting to test a current state's outcomes
    with open("saved_level.json", "w") as f:
        json.dump(nextStates[0], f) #change 0 with number of state you want to visit

main()"""