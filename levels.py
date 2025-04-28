import tkinter as tk
from tkinter import PhotoImage
import json
from PIL import Image, ImageTk

#-1 - empty space
#0 - Johnny
#1 - brick
#2 - helmet
#3 - crate
#4 - water
#5 - ladder
#6 - roof
#7 - still helmet
#Levels are stored in the form:
#[[[-1, 1], [-1, 1], [-1, 1]],
# [[-1, 1], [-1, 0], [-1, 1]],
# [[-1, 1], [-1, 1], [-1, 1]]]
#Each cell is a list becasue a cell can contain Johnny and a ladder
#Each cell contains an empty tile to account for moving objects. eg Johnny
#Doesn't need an empty tile in each cell, however, the way the grid was initially constructed required it. This changed when removing tiles was added
#Methods were created with having a -1 in every list in mind

try:
    with open("saved_level.json", "r") as fload:
        level = json.load(fload)
        #Ensure all cells are lists (in case some are integers like -1 or 0)
        for y in range(len(level)):
            for x in range(len(level[y])):
                if not isinstance(level[y][x], list):
                    level[y][x] = [level[y][x]]  #Convert single integers to a list
except:
    level = [[[-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1]], [[-1, 1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1], [-1, 1]], [[-1, 1], [-1], [-1, 0], [-1], [-1], [-1], [-1, 3], [-1], [-1], [-1, 2], [-1, 1]], [[-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1, 1], [-1], [-1, 1], [-1, 1], [-1, 1]], [[-1], [-1], [-1], [-1], [-1], [-1], [-1, 1], [-1, 1], [-1, 1], [-1], [-1]]]  #Default level if the file doesn't exist or is empty


root = tk.Tk()
filepath = "Assets/"

#Resize the images
def load_image(file):
    size = (50, 50)
    img = Image.open(file)
    img = img.resize(size)
    return ImageTk.PhotoImage(img)

images = {
    -1: load_image(filepath + "Empty.png"),
    0: load_image(filepath + "Johnny.png"),
    1: load_image(filepath + "Brick.png"),
    2: load_image(filepath + "Helmet.png"),
    3: load_image(filepath + "Crate.png"),
    4: load_image(filepath + "Water.png"),
    5: load_image(filepath + "Ladder.png"),
    6: load_image(filepath + "Roof.png"),
    7: load_image(filepath + "StillHelmet.png")
}

cellSize = 50

canvas = tk.Canvas(root)
canvas.grid(row=0, column=0, columnspan=5)


def update_canvas():
    global canvas
    gridWidth = len(level[0])
    gridHeight = len(level)
    canvas.config(width=gridWidth * cellSize, height=gridHeight * cellSize)
    draw_grid()


chosenType = -1
def choose_type(cellType, button):
    global chosenType
    chosenType = cellType
    highlight_button(button)


def draw_type(event):
    x = event.x // cellSize
    y = event.y // cellSize
    if chosenType not in level[y][x]:
        level[y][x].append(chosenType)
    draw_grid()


def remove_type(event):
    x = event.x // cellSize
    y = event.y // cellSize
    if chosenType in level[y][x]: 
        level[y][x].remove(chosenType)
    draw_grid()


def draw_grid():
    canvas.delete("all")  #Clear the canvas
    for y, row in enumerate(level):  #Iterate through the rows
        for x, cell in enumerate(row):  #Iterate through the columns (cells)
            for type in cell:  #For each block in the cell (it could be more than one)
                img = images[type]
                canvas.create_image(x * cellSize, y * cellSize, anchor="nw", image=img)


def highlight_button(button):
    for x in allButtons:
        x.config(bg="SystemButtonFace")
    button.config(bg="lightblue")


def decrease_level_height():
    del level[len(level) - 1]
    update_canvas()


def decrease_level_width():
    for row in level:
        del row[len(row) - 1]
    update_canvas()


def increase_level_height():
    level.append([[-1] for _ in range(len(level[0]))])  #Creates a unique list instead of a shared list
    update_canvas()


def increase_level_width():
    for row in level:
        row.append([-1])
    update_canvas()


def save_level():
    with open("saved_level.json", "w") as f:
        json.dump(level, f)


#Left click triggers event to place blocks
canvas.bind("<Button-1>", draw_type)
#Right click triggers event to remove blocks
canvas.bind("<Button-3>", remove_type)

#Group selection buttons together
selectFrame = tk.Frame(root)
selectFrame.grid(row=1, column=0, columnspan=5, pady=10)

#Create buttons for changing the type of block
emptyButton = tk.Button(selectFrame, text="Empty", command=lambda: choose_type(-1, emptyButton))
emptyButton.grid(row=0, column=0)
johnnyButton = tk.Button(selectFrame, text="Johnny", command=lambda: choose_type(0, johnnyButton))
johnnyButton.grid(row=0, column=1)
brickButton = tk.Button(selectFrame, text="Brick", command=lambda: choose_type(1, brickButton))
brickButton.grid(row=0, column=2)
helmetButton = tk.Button(selectFrame, text="Helmet", command=lambda: choose_type(2, helmetButton))
helmetButton.grid(row=0, column=3)
crateButton = tk.Button(selectFrame, text="Crate", command=lambda: choose_type(3, crateButton))
crateButton.grid(row=0, column=4)
waterButton = tk.Button(selectFrame, text="Water", command=lambda: choose_type(4, waterButton))
waterButton.grid(row=0, column=5)
ladderButton = tk.Button(selectFrame, text="Ladder", command=lambda: choose_type(5, ladderButton))
ladderButton.grid(row=0, column=6)
roofButton = tk.Button(selectFrame, text="Roof", command=lambda: choose_type(6, roofButton))
roofButton.grid(row=0, column=7)
stillHelmetButton = tk.Button(selectFrame, text="Still Helmet", command=lambda: choose_type(7, stillHelmetButton))
stillHelmetButton.grid(row=0, column=8)
#Add all buttons to a list for highlighting
allButtons = [emptyButton, johnnyButton, brickButton, helmetButton, crateButton, waterButton, ladderButton, roofButton, stillHelmetButton]

#Group resize buttons together
resizeFrame = tk.Frame(root)
resizeFrame.grid(row=3, column=0, columnspan=5, pady=10)

#Create buttons for adding and removing columns and edges
addRowButton = tk.Button(resizeFrame, text="Add Row", command=lambda: increase_level_height())
addRowButton.grid(row=0, column=0)
addColButton = tk.Button(resizeFrame, text="Add Col", command=lambda: increase_level_width())
addColButton.grid(row=0, column=5)
delRowButton = tk.Button(resizeFrame, text="Del Row", command=lambda: decrease_level_height())
delRowButton.grid(row=1, column=0)
delColButton = tk.Button(resizeFrame, text="Del Col", command=lambda: decrease_level_width())
delColButton.grid(row=1, column=5)

#Create button for saving
saveButton = tk.Button(root, text="Save Level", command=lambda: save_level())
saveButton.grid(row=4, column=0, columnspan=5, pady=10)


update_canvas()

root.mainloop()
