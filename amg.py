#!/usr/bin/env python

# - ascii map generator

import random

# - Lists of rectangles
shapes0 = {
    1:{"cols": 1, "rows": 1},
    2:{"cols": 1, "rows": 2},
    3:{"cols": 2, "rows": 1}
}

shapes1 = {
    1:{"cols": 10, "rows": 10},
    2:{"cols": 15, "rows": 8},
    3:{"cols": 7, "rows": 3},
    4:{"cols": 12, "rows": 5},
    5:{"cols": 20, "rows": 2}
}

shapes2 = {
    1:{"cols": 30, "rows": 5},
    2:{"cols": 20, "rows": 6},
    3:{"cols": 25, "rows": 5}
}

shapes3 = {
    1:{"cols": 10, "rows": 50},
    2:{"cols": 15, "rows": 75},
    3:{"cols": 5, "rows": 100}
}

shapes4 = {
    1:{"cols": 7, "rows": 2},
    2:{"cols": 6, "rows": 3},
    3:{"cols": 5, "rows": 4}
}

shapes5 = {
    1:{"cols": 70, "rows": 30}
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
    global mapGlyphs
    global map_pins 
    global pinsInLegend
    global legend 
    global shapes
    global presets
    global numberOfIslands
    global length
    global width
    global numberOfCuts
    global LS 
    global RS
    global placeMapPins
    map_pins = ["*", "@", "!", ".", "+", "%", "&", "$", "#"]
    pinsInLegend = []
    mapGlyphs = {}
    for i in presets:
        if presets[i]["Set"] == cmd:
            shapes = presets[i]["shapes"]
            numberOfIslands = presets[i]["numberOfIslands"]
            numberOfCuts = presets[i]["numberOfCuts"]
            length = presets[i]["length"]
            width = presets[i]["width"]
            placeMapPins = presets[i]["placeMapPins"]
    for x in range(length*width):
        mapGlyphs[x] = "~"
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
    global mapGlyphs
    global legend
    c = 0
    for i in range(length):
        for x in range(width):
            print(mapGlyphs[c], end = "")
            c += 1
        print(legend[i])

# Function that checks if you can place a specified rectangle(Box) on a specified position(x)
def CPlaceB(x):
    global mapGlyphs
    global Box
    global length
    global width
    y = int(x/width) + 1
    t = x - ((y - 1)*width)
    return ((t + shapes[Box]["cols"]) <= width and (y + shapes[Box]["rows"]) <= length)

# Function that places Box on x
def PlaceB(i):
    global Box
    global width
    global mapGlyphs
    for y in range(shapes[Box]["rows"]):
        for x in range(shapes[Box]["cols"]):
            mapGlyphs[i] = "#"
            i +=1
        i += (width - shapes[Box]["cols"])

# Function that randomly picks a location/rectangle(box)
def AddB():
    global Box
    global length
    global width
    Box = random.choice(list(shapes.keys()))
    while True:
            i = random.randint(-1,(length*width))
            if CPlaceB(i) == True:
                PlaceB(i)
                return None

# Function that smooths out long corners
def carveEdges():
    global mapGlyphs
    global width
    global numberOfCuts
    global RS
    global LS
    t = 0
    while t <= numberOfCuts:
        t += 1
        for i in mapGlyphs:
            if mapGlyphs[i] == "#":
                sides = 0
                try: #up
                    glyph = mapGlyphs[i-width]
                except:
                    glyph = "~"
                if glyph == "~":
                    sides += 1

                try: #down
                    glyph = mapGlyphs[i+width]
                except:
                    glyph = "~"
                if glyph == "~":
                    sides += 1

                if i in LS: #left
                    sides += 1
                else:
                    try:
                        glyph = mapGlyphs[i-1]
                    except:
                        glyph = "~"
                    if glyph == "~":
                        sides += 1

                if i in RS: #right
                    sides += 1
                else:
                    try:
                        glyph = mapGlyphs[i+1]
                    except:
                        glyph = "~"
                    if glyph == "~":
                        sides += 1

                cutChances = {
                    0: 0.0,
                    1: 0.0196078431372549,
                    2: 0.75,
                    3: 0.8333333333333334,
                    4: 1.0
                }

                if sides == 4:
                    mapGlyphs[i] = "~"
                elif random.random() < cutChances[sides]:
                    mapGlyphs[i] = "~"

# Function that replaces the outline of the rectangles with ascii art
def outlineIslands():
    global mapGlyphs
    global width
    global LS
    global RS
    for i in mapGlyphs:
        if mapGlyphs[i] == "#":
            Sides = {"U": False, "D": False, "L": False, "R": False}
            try: #up
                glyph = mapGlyphs[i-width]
            except:
                glyph = "~"
            Sides["U"] = (glyph == "~")

            try: #down
                glyph = mapGlyphs[i+width]
            except:
                glyph = "~"
            Sides["D"] = (glyph == "~")

            try: #left
                glyph = mapGlyphs[i-1]
            except:
                glyph = mapGlyphs[i] #'#'
            Sides["L"] = (glyph == "~") or (i in LS)

            try: #right
                glyph = mapGlyphs[i+1]
            except:
                glyph = mapGlyphs[i] #'#'
            Sides["R"] = (glyph == "~") or (i in RS)

            if Sides["U"] and Sides["D"] and Sides["R"]:
                mapGlyphs[i] = ">"  
            elif Sides["U"] and Sides["D"] and Sides["L"]:   
                mapGlyphs[i] = "<"
            elif Sides["U"] and Sides["R"] and Sides["L"]:   
                mapGlyphs[i] = "^"
            elif Sides["R"] and Sides["D"] and Sides["L"]:   
                mapGlyphs[i] = "v"
            elif (Sides["U"] and Sides["L"]) or (Sides["D"] and Sides["R"]):
                mapGlyphs[i] = "/"
            elif (Sides["U"] and Sides["R"]) or (Sides["D"] and Sides["L"]):
                mapGlyphs[i] = u"\u005C"
            elif Sides["U"]:
                mapGlyphs[i] = u"\u203E"
            elif Sides["D"]:
                mapGlyphs[i] = "_"
            elif Sides["L"] or Sides["R"]:
                mapGlyphs[i] = "|"
            else:
                pass

# Function that clears out overything but the sea and outline
def whitespaceLand():
    global mapGlyphs
    for i in mapGlyphs:
        if mapGlyphs[i] == "#":
            mapGlyphs[i] = " "

# Function that adds random stuff to the empty parts of the map
def placePins():
    global mapGlyphs
    global pinsInLegend
    global map_pins 
    global placeMapPins
    if placeMapPins == "T":
        for i in mapGlyphs:
            if mapGlyphs[i] == " ":
                if random.randint(0, 25) == 1:
                    mapGlyphs[i] = random.choice(map_pins)
                    if mapGlyphs[i] not in pinsInLegend:
                        pinsInLegend.append(mapGlyphs[i])
                    if mapGlyphs[i] in ["@", "&", "+", "%", "#"]:
                        map_pins.remove(mapGlyphs[i])

def createLegend():
    global pinsInLegend
    global legend
    global mapGlyphs
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
    for p in pinsInLegend:
        legend.append(" | " + p + " = " + Meaning[p])
    for i in range(len(legend), length-1):
        legend.append(" |                      |")
    legend.append(" +----------------------+")
    mapGlyphs[width + 2] = "N"
    mapGlyphs[width*2 + 1] = "W"
    mapGlyphs[width*2 + 2] = "+"
    mapGlyphs[width*2 + 3] = "E"
    mapGlyphs[width*3 + 2] = "S"
        

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
