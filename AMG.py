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
    "1 - Pocket sized" : {"Set": 1, "length": 15, "width": 25, "shapes": shapes1, "numberOfCuts": 2, "numberOfIslands": 5, "placeMapPins": "T"},
    "2 - Long" : {"Set": 2, "length": 500, "width": 100, "shapes": shapes3, "numberOfCuts": 3, "numberOfIslands": 100, "placeMapPins": "T"},
    "3 - Mess" : {"Set": 3, "length": 36, "width": 100, "shapes": shapes0, "numberOfCuts": 0, "numberOfIslands": 1000, "placeMapPins": "F"},
    "4 - Box" : {"Set": 4, "length": 36, "width": 100, "shapes": shapes2, "numberOfCuts": 0, "numberOfIslands": 20, "placeMapPins": "T"},
    "5 - Islands" : {"Set": 5, "length": 25, "width": 75, "shapes": shapes4, "numberOfCuts": 0, "numberOfIslands": 25, "placeMapPins": "T"},
    "6 - Waterland" : {"Set": 6, "length": 20, "width": 50, "shapes": shapes0, "numberOfCuts": 1, "numberOfIslands": 1500, "placeMapPins": "F"},
    "7 - Blob" : {"Set": 7, "length": 36, "width": 100, "shapes": shapes5, "numberOfCuts": 20, "numberOfIslands": 3, "placeMapPins": "F"},
}

# Function that creates the basic map, defines stuff like size, legend, positions on left/right side, ect
def Start(s):
    global MAP
    global map_pins 
    global PIL
    global Legend 
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
    if s == "1":
        shapes = shapes1
        numberOfIslands = 7
        numberOfCuts = 2
        length = 18
        width = 40
        placeMapPins = "T"
    elif s == "2":
        shapes = shapes2
        numberOfIslands = 15
        numberOfCuts = 3
        length = 36
        width = 100
        placeMapPins = "T"
    elif s == "3":
        shapes = shapes2
        numberOfIslands = 50
        numberOfCuts = 4
        length = 48
        width = 191
        placeMapPins = "T"
    else:
        for i in presets:
            print(i)
        cmd = int(input(">"))
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
    i = 0
    y = 0
    while i != length:
        y += width
        LS.append(y)
        i += 1
    i = 0
    y = 0
    while i != length:
        y += width
        RS.append(y)
        i += 1

# Function that prints the map to the console
def PrintM():
    global length
    global width
    global MAP
    global Legend
    c = 0
    x = 0
    i = 0
    for i in range(length):
        for x in range(width):
            print(MAP[c], end = "")
            x += 1
            c += 1
        try:
            print(Legend[i])
        except:
            print(" |                      |")
        x = 1
        i += 1

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
    y = 0
    x = 0
    while y != shapes[Box]["y"]:
        while x != shapes[Box]["x"]:
            MAP[i] = "#"
            i +=1
            x += 1
        i += (width - shapes[Box]["x"])
        y += 1
        x = 0

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
def Curve():
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
def Outline():
    global MAP
    global width
    global LS
    global RS
    for i in MAP:
        if MAP[i] == "#":
            Sides = {"U": 0, "D": 0, "L": 0, "R": 0}
            # - U
            x = i - width
            try:
                a = MAP[x]
            except:
                a = "~"
            if a == "~":
                Sides["U"] = 1
            # - U
            # - D
            x = i + width
            try:
                a = MAP[x]
            except:
                a = "~"
            if a == "~":
                Sides["D"] = 1
            # - D
            # - L
            if i in LS:
                Sides["L"] = 1
            else:
                x = i - 1
                try:
                    a = MAP[x]
                except:
                    a = MAP[i]
                if a == "~":
                    Sides["L"] = 1
            # - L
            # - R
            if i in RS:
                Sides["R"] = 1
            else:
                x = i + 1
                try:
                    a = MAP[x]
                except:
                    a = MAP[i]
                if a == "~":
                    Sides["R"] = 1
            # - R
            if Sides["U"] == 1 and Sides["D"] == 1 and Sides["R"] == 1:
                MAP[i] = ">"  
            elif Sides["U"] == 1 and Sides["D"] == 1 and Sides["L"] == 1:   
                MAP[i] = "<"
            elif Sides["U"] == 1 and Sides["R"] == 1 and Sides["L"] == 1:   
                MAP[i] = "^"
            elif Sides["R"] == 1 and Sides["D"] == 1 and Sides["L"] == 1:   
                MAP[i] = "v"
            elif (Sides["U"] == 1 and Sides["L"] == 1) or (Sides["D"] == 1 and Sides["R"] == 1):
                MAP[i] = "/"
            elif (Sides["U"] == 1 and Sides["R"] == 1) or (Sides["D"] == 1 and Sides["L"] == 1):
                MAP[i] = u"\u005C"
            elif Sides["U"] == 1:
                MAP[i] = u"\u203E"
            elif Sides["D"] == 1:
                MAP[i] = "_"
            elif Sides["L"] == 1 or Sides["R"] == 1:
                MAP[i] = "|"
            else:
                pass

# Function that clears out overything but the sea and outline
def Clear():
    global MAP
    for i in MAP:
        if MAP[i] == "#":
            MAP[i] = " "

# Function that adds random stuff to the empty parts of the map
def AddStuff():
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

# Function that creats the Legend
def LegendC():
    global PIL
    global Legend
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
    Legend = {
        0: " +----------------------+",
        1: " |        " + Name + "        |",
        2: " +----------------------+"
    }
    n = 4
    for i in PIL:
        Legend[n] = " | " + i + " = " + Meaning[i]
        n += 1
    Legend[length - 1] = " +----------------------+"
    MAP[width + 2] = "N"
    MAP[width*2 + 1] = "W"
    MAP[width*2 + 2] = "+"
    MAP[width*2 + 3] = "E"
    MAP[width*3 + 2] = "S"
        

def main():
    while True:
        print("Small(1), Medium(2), or Large(3)")
        print("More(4)")
        cmd = input(">")
        Start(cmd)
        for i in range(numberOfIslands):
            AddB()
        print("")
        Curve()
        Outline()
        Clear()
        AddStuff()
        LegendC()
        PrintM()
        print("")

if __name__ == "__main__":
    main()
