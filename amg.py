#!/usr/bin/env python

# - ascii map generator

import random

# - Lists of rectangles
shapes0 = {
    1:{"x": 1, "y": 1},
    2:{"x": 1, "y": 2},
    3:{"x": 2, "y": 1}
}

shapes1 = {
    1:{"x": 10, "y": 10},
    2:{"x": 15, "y": 8},
    3:{"x": 7, "y": 3},
    4:{"x": 12, "y": 5},
    5:{"x": 20, "y": 2}
}

shapes2 = {
    1:{"x": 30, "y": 5},
    2:{"x": 20, "y": 6},
    3:{"x": 25, "y": 5}
}

shapes3 = {
    1:{"x": 10, "y": 50},
    2:{"x": 15, "y": 75},
    3:{"x": 5, "y": 100}
}

shapes4 = {
    1:{"x": 7, "y": 2},
    2:{"x": 6, "y": 3},
    3:{"x": 5, "y": 4}
}

shapes5 = {
    1:{"x": 70, "y": 30}
}

presets = {
    "1 - Small" : {"Set": '1', "length": 18, "width": 40, "shapes": shapes1, "numberOfCuts": 2, "numberOfIslands": 7, "placeMapPins": "T"},
    "2 - Medium" : {"Set": '2', "length": 36, "width": 100, "shapes": shapes2, "numberOfCuts": 3, "numberOfIslands": 15, "placeMapPins": "T"},
    "3 - Large" : {"Set": '3', "length": 48, "width": 191, "shapes": shapes2, "numberOfCuts": 4, "numberOfIslands": 50, "placeMapPins": "T"},
    "4 - Pocket sized" : {"Set": '4', "length": 15, "width": 25, "shapes": shapes1, "numberOfCuts": 2, "numberOfIslands": 5, "placeMapPins": "T"},
    "5 - Long" : {"Set": '5', "length": 500, "width": 100, "shapes": shapes3, "numberOfCuts": 3, "numberOfIslands": 100, "placeMapPins": "T"},
    "6 - Mess" : {"Set": '6', "length": 36, "width": 100, "shapes": shapes0, "numberOfCuts": 0, "numberOfIslands": 1000, "placeMapPins": "F"},
    "7 - Box" : {"Set": '7', "length": 36, "width": 100, "shapes": shapes2, "numberOfCuts": 0, "numberOfIslands": 20, "placeMapPins": "T"},
    "8 - Islands" : {"Set": '8', "length": 25, "width": 75, "shapes": shapes4, "numberOfCuts": 0, "numberOfIslands": 25, "placeMapPins": "T"},
    "9 - Waterland" : {"Set": '9', "length": 20, "width": 50, "shapes": shapes0, "numberOfCuts": 1, "numberOfIslands": 1500, "placeMapPins": "F"},
    "0 - Blob" : {"Set": '0', "length": 36, "width": 100, "shapes": shapes5, "numberOfCuts": 20, "numberOfIslands": 3, "placeMapPins": "F"},
}

# Function that creates the basic map, defines stuff like size, legend, positions on left/right side, ect
def Start(cmd):
    global MAP
    global map_pins 
    global PIL
    global legend 
    global shapes
    global presets
    global numberOfIslands
    global length
    global width
    global A
    global numberOfCuts
    global LS 
    global RS
    global placeMapPins
    map_pins = ["*", "@", "!", ".", "+", "%", "&", "$", "#"]
    PIL = []
    MAP = {}
    for i in presets:
        if presets[i]["Set"] == cmd:
            shapes = presets[i]["shapes"]
            numberOfIslands = presets[i]["numberOfIslands"]
            numberOfCuts = presets[i]["numberOfCuts"]
            length = presets[i]["length"]
            width = presets[i]["width"]
            placeMapPins = presets[i]["placeMapPins"]
    A = length*width
    MAP = {}
    for x in range(A):
        MAP[x] = "~"
    RS = [width]
    LS = [0]
    y = 0
    for i in range(length):
        y += width
        LS.append(y)
    y = 0
    for i in range(length):
        y += width
        RS.append(y)

# print the map 
def display():
    global length
    global width
    global MAP
    global legend
    c = 0
    x = 0
    i = 0
    for i in range(length):
        for x in range(width):
            print(MAP[c], end = "")
            c += 1
        print(legend[i])

# Function that checks if you can place a specified rectangle(Box) on a specified position(x)
def CPlaceB(x):
    global MAP
    global Box
    global length
    global width
    y = int(x/width) + 1
    t = x - ((y - 1)*width)
    return ((t + shapes[Box]["x"]) <= width and (y + shapes[Box]["y"]) <= length)

# Function that places Box on x
def PlaceB(i):
    global Box
    global width
    global MAP
    for y in range(shapes[Box]["y"]):
        for x in range(shapes[Box]["x"]):
            MAP[i] = "#"
            i +=1
        i += (width - shapes[Box]["x"])

# Function that randomly picks a location/rectangle(box)
def AddB():
    global Box
    global A
    Box = random.choice(list(shapes.keys()))
    while True:
            i = random.randint(-1,(A))
            if CPlaceB(i) == True:
                PlaceB(i)
                return None

# Function that smooths out long corners
def carveEdges():
    global MAP
    global width
    global numberOfCuts
    global RS
    global LS
    t = 0
    while t <= numberOfCuts:
        t += 1
        for i in MAP:
            if MAP[i] == "#":
                Sides = 0
                # - U
                x = i - width
                try:
                    a = MAP[x]
                except:
                    a = "~"
                if a == "~":
                    Sides += 1
                # - U
                # - D
                x = i + width
                try:
                    a = MAP[x]
                except:
                    a = "~"
                if a == "~":
                    Sides += 1
                # - D
                # - L
                if i in LS:
                    Sides += 1
                else:
                    x = i - 1
                    try:
                        a = MAP[x]
                    except:
                        a = "~"
                    if a == "~":
                        Sides += 1
                # - L
                # - R
                if i in RS:
                    Sides += 1
                else:
                    x = i + 1
                    try:
                        a = MAP[x]
                    except:
                        a = "~"
                    if a == "~":
                        Sides += 1
                # - R
                if Sides == 4:
                    MAP[i] = "~"
                elif Sides == 1 and t <= numberOfCuts:
                    if random.randint(0, 50) == 1:
                        MAP[i] = "~"
                elif Sides == 2 and t <= numberOfCuts:
                    if random.randint(0, 3) != 1:
                        MAP[i] = "~"
                elif Sides == 3 and t <= numberOfCuts:
                    if random.randint(0, 5) != 1:
                        MAP[i] = "~"
                else:
                    pass

# Function that replaces the outline of the rectangles with ascii art
def outlineIslands():
    global MAP
    global width
    global LS
    global RS
    for i in MAP:
        if MAP[i] == "#":
            Sides = {"U": False, "D": False, "L": False, "R": False}
            try: #up
                glyph = MAP[i-width]
            except:
                glyph = "~"
            Sides["U"] = (glyph == "~")

            try: #down
                glyph = MAP[i+width]
            except:
                glyph = "~"
            Sides["D"] = (glyph == "~")

            try: #left
                glyph = MAP[i-1]
            except:
                glyph = MAP[i] #'#'
            Sides["L"] = (glyph == "~") or (i in LS)

            try: #right
                glyph = MAP[i+1]
            except:
                glyph = MAP[i] #'#'
            Sides["R"] = (glyph == "~") or (i in RS)

            if Sides["U"] and Sides["D"] and Sides["R"]:
                MAP[i] = ">"  
            elif Sides["U"] and Sides["D"] and Sides["L"]:   
                MAP[i] = "<"
            elif Sides["U"] and Sides["R"] and Sides["L"]:   
                MAP[i] = "^"
            elif Sides["R"] and Sides["D"] and Sides["L"]:   
                MAP[i] = "v"
            elif (Sides["U"] and Sides["L"]) or (Sides["D"] and Sides["R"]):
                MAP[i] = "/"
            elif (Sides["U"] and Sides["R"]) or (Sides["D"] and Sides["L"]):
                MAP[i] = u"\u005C"
            elif Sides["U"]:
                MAP[i] = u"\u203E"
            elif Sides["D"]:
                MAP[i] = "_"
            elif Sides["L"] or Sides["R"]:
                MAP[i] = "|"
            else:
                pass

# Function that clears out overything but the sea and outline
def whitespaceLand():
    global MAP
    for i in MAP:
        if MAP[i] == "#":
            MAP[i] = " "

# Function that adds random stuff to the empty parts of the map
def placePins():
    global MAP
    global PIL
    global map_pins 
    global placeMapPins
    if placeMapPins == "T":
        for i in MAP:
            if MAP[i] == " ":
                if random.randint(0, 25) == 1:
                    MAP[i] = random.choice(map_pins)
                    if MAP[i] not in PIL:
                        PIL.append(MAP[i])
                    if MAP[i] in ["@", "&", "+", "%", "#"]:
                        map_pins.remove(MAP[i])

def createLegend():
    global PIL
    global legend
    global MAP
    global width
    Name  = random.choice(["Str","Tra","Kle","Olc", "Mat", "Wir", "Sle", "Pad", "Lat"]) + \
            random.choice(["ait","cre","zat","tor", "lin", "dly", "waz", "ken", "mon"])
    Hname = random.choice(["Mikker","Wimmly","Jarmit", "FiFyFo", "Peeter", "Nipnoe", "Padfot", "??????"]) + \
            " the " + \
            random.choice(["Bold  |","Stong |","Fast  |","Large |", "Small |", "Fat   |", "Stuped|", "Smart |", "Fine  |"])
    Dname = random.choice(["Scar             |", \
                           "Kainto           |", \
                           "Flea             |", \
                           "Botron           |", \
                           "Frot             |", \
                           "Clotenomen       |", \
                           "Fimotrin         |", \
                           "Death            |"])
    Meaning = {
    "*": "Lake             |",
    "@": Hname,
    "!": "Battle           |",
    ".": "Mountain         |",
    "+": "Mintar           |",
    "%": "Thraf            |",
    "&": Dname,
    "#": "Impom            |",
    "$": "Gold             |"
    }
    legend = [
        " +----------------------+",
        " |        " + Name + "        |",
        " +----------------------+",
        " |                      |"
    ]
    for i in PIL:
        legend.append(" | " + i + " = " + Meaning[i])
    for i in range(len(legend), length-1):
        legend.append(" |                      |")
    legend.append(" +----------------------+")
    MAP[width + 2] = "N"
    MAP[width*2 + 1] = "W"
    MAP[width*2 + 2] = "+"
    MAP[width*2 + 3] = "E"
    MAP[width*3 + 2] = "S"
        

def main():
    while True:
        for i in presets:
            print(i)
        cmd = input(">")
        Start(cmd)
        for i in range(numberOfIslands):
            AddB()
        print("")
        carveEdges()
        outlineIslands()
        whitespaceLand()
        placePins()
        createLegend()
        display()
        print("")

if __name__ == "__main__":
    main()
