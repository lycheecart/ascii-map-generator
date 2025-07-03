#!/usr/bin/env python

# - ascii map generator

import random

class Rect:
    def __init__(self, rows=0, cols=0):
        self.rows = rows 
        self.cols = cols

class Config:
    def __init__(self, selectIndicator=None, selectKey=None,length=0,width=0,shapes=[],numberOfCuts=0,numberOfIslands=0,placeMapPins=False):
        self.menu = []
        self.selectIndicator=selectIndicator
        self.selectKey=selectKey
        self.length=length
        self.width=width
        self.shapes=shapes 
        self.numberOfCuts=numberOfCuts
        self.numberOfIslands=numberOfIslands
        self.placeMapPins=placeMapPins

    def loadOptions(self):
        self.menu.append(Config(
            selectIndicator="1 - Small", selectKey='1', length=18, width=40,
            shapes = [
                Rect(rows=10, cols=10), 
                Rect(rows=8,  cols=15), 
                Rect(rows=3,  cols=7), 
                Rect(rows=5,  cols=12),
                Rect(rows=2,  cols=20)
            ], 
            numberOfCuts=2, numberOfIslands=7, placeMapPins="T"))
        self.menu.append(Config(
            selectIndicator="2 - Medium", selectKey='2', length=36, width=100,
            shapes = [
                Rect(rows=5,  cols=30),
                Rect(rows=6,  cols=20),
                Rect(rows=5,  cols=25)
            ],
            numberOfCuts=3,numberOfIslands=15,placeMapPins="T"))
        self.menu.append(Config(
            selectIndicator="3 - Large", selectKey='3', length=48, width=191,
            shapes = [
                Rect(rows=5,  cols=30),
                Rect(rows=6,  cols=20),
                Rect(rows=5,  cols=25)
            ],
            numberOfCuts=4,numberOfIslands=50,placeMapPins="T"))
        self.menu.append(Config(
            selectIndicator="4 - Pocket sized", selectKey='4', length=15, width=25,
            shapes = [
                Rect(rows=10, cols=10), 
                Rect(rows=8,  cols=15), 
                Rect(rows=3,  cols=7), 
                Rect(rows=5,  cols=12),
                Rect(rows=2,  cols=20)
            ],
            numberOfCuts=2,numberOfIslands=5,placeMapPins="T"))
        self.menu.append(Config(
            selectIndicator="5 - Long", selectKey='5', length=500, width=100,
            shapes = [
                Rect(rows=50,  cols=10),
                Rect(rows=75,  cols=15),
                Rect(rows=100,  cols=5)
            ],
            numberOfCuts=3,numberOfIslands=100,placeMapPins="T"))
        self.menu.append(Config(
            selectIndicator="6 - Mess", selectKey='6', length=36, width=100,
            shapes = [
                Rect(rows=1, cols=1),
                Rect(rows=2, cols=1),
                Rect(rows=1, cols=2)
            ],
            numberOfCuts=0,numberOfIslands=1000,placeMapPins="F"))
        self.menu.append(Config(
            selectIndicator="7 - Box", selectKey='7', length=36, width=100,
            shapes = [
                Rect(rows=5,  cols=30),
                Rect(rows=6,  cols=20),
                Rect(rows=5,  cols=25)
            ],
            numberOfCuts=0,numberOfIslands=20,placeMapPins="T"))
        self.menu.append(Config(
            selectIndicator="8 - Islands", selectKey='8', length=25, width=75,
            shapes = [
                Rect(rows=2,  cols=7),
                Rect(rows=3,  cols=6),
                Rect(rows=4,  cols=5)
            ],
            numberOfCuts=0,numberOfIslands=25,placeMapPins="T"))
        self.menu.append(Config(
            selectIndicator="9 - Waterland", selectKey='9', length=20, width=50,
            shapes = [
                Rect(rows=1, cols=1),
                Rect(rows=2, cols=1),
                Rect(rows=1, cols=2)
            ],
            numberOfCuts=1,numberOfIslands=1500,placeMapPins="F"))
        self.menu.append(Config(
            selectIndicator="0 - Blob", selectKey='0', length=36, width=100,
            shapes = [
                Rect(rows=30,  cols=70)
            ],
            numberOfCuts=20,numberOfIslands=3,placeMapPins="F"))

class Mapper:
    def configureFromInput(self, cmd):
        self.map_pins = ["*", "@", "!", ".", "+", "%", "&", "$", "#"]
        self.pinsInLegend = []
        self.mapGlyphs = {}
        conf = Config()
        conf.loadOptions()
        for config in conf.menu:
            if config.selectKey == cmd:
                self.shapes = config.shapes
                self.numberOfIslands = config.numberOfIslands
                self.numberOfCuts = config.numberOfCuts
                self.length = config.length
                self.width = config.width
                self.placeMapPins = config.placeMapPins
        for x in range(self.length * self.width):
            self.mapGlyphs[x] = "~"
        self.LS = [0]
        self.RS = [self.width]
        y = 0
        for i in range(self.length):
            y += self.width
            self.LS.append(y)
        y = 0
        for i in range(self.length):
            y += self.width
            self.RS.append(y)

    def display(self):
        c = 0
        for i in range(self.length):
            for x in range(self.width):
                print(self.mapGlyphs[c], end = "")
                c += 1
            print(self.legend[i])

    def checkIslandBounds(self, x):
        y = int(x/self.width) + 1
        t = x - ((y - 1)*self.width)
        selectedShape = self.shapes[self.shapeI]
        return ((t + selectedShape.cols <= self.width and (y + selectedShape.rows <= self.length)))

    def placeIsland(self,i):
        selectedShape = self.shapes[self.shapeI]
        for y in range(selectedShape.rows):
            for x in range(selectedShape.cols):
                self.mapGlyphs[i] = "#"
                i +=1
            i += (self.width - selectedShape.cols)

    def addIsland(self):
        self.shapeI = random.randint(0,len(self.shapes)-1)
        while True:
                i = random.randint(-1, (self.length * self.width))
                if self.checkIslandBounds(i) == True:
                    self.placeIsland(i)
                    return None

    def carveEdges(self):
        t = 0
        while t <= self.numberOfCuts:
            t += 1
            for i in self.mapGlyphs:
                if self.mapGlyphs[i] == "#":
                    sides = 0
                    try: #up
                        glyph = self.mapGlyphs[i-self.width]
                    except:
                        glyph = "~"
                    if glyph == "~":
                        sides += 1

                    try: #down
                        glyph = self.mapGlyphs[i+self.width]
                    except:
                        glyph = "~"
                    if glyph == "~":
                        sides += 1

                    if i in self.LS: #left
                        sides += 1
                    else:
                        try:
                            glyph = self.mapGlyphs[i-1]
                        except:
                            glyph = "~"
                        if glyph == "~":
                            sides += 1

                    if i in self.RS: #right
                        sides += 1
                    else:
                        try:
                            glyph = self.mapGlyphs[i+1]
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
                        self.mapGlyphs[i] = "~"
                    elif random.random() < cutChances[sides]:
                        self.mapGlyphs[i] = "~"

    def outlineIslands(self):
        for i in self.mapGlyphs:
            if self.mapGlyphs[i] == "#":
                sides = {"U": False, "D": False, "L": False, "R": False}
                try: #up
                    glyph = self.mapGlyphs[i-self.width]
                except:
                    glyph = "~"
                sides["U"] = (glyph == "~")

                try: #down
                    glyph = self.mapGlyphs[i+self.width]
                except:
                    glyph = "~"
                sides["D"] = (glyph == "~")

                try: #left
                    glyph = self.mapGlyphs[i-1]
                except:
                    glyph = self.mapGlyphs[i] #'#'
                sides["L"] = (glyph == "~") or (i in self.LS)

                try: #right
                    glyph = self.mapGlyphs[i+1]
                except:
                    glyph = self.mapGlyphs[i] #'#'
                sides["R"] = (glyph == "~") or (i in self.RS)

                if sides["U"] and sides["D"] and sides["R"]:
                    self.mapGlyphs[i] = ">"  
                elif sides["U"] and sides["D"] and sides["L"]:   
                    self.mapGlyphs[i] = "<"
                elif sides["U"] and sides["R"] and sides["L"]:   
                    self.mapGlyphs[i] = "^"
                elif sides["R"] and sides["D"] and sides["L"]:   
                    self.mapGlyphs[i] = "v"
                elif (sides["U"] and sides["L"]) or (sides["D"] and sides["R"]):
                    self.mapGlyphs[i] = "/"
                elif (sides["U"] and sides["R"]) or (sides["D"] and sides["L"]):
                    self.mapGlyphs[i] = u"\u005C"
                elif sides["U"]:
                    self.mapGlyphs[i] = u"\u203E"
                elif sides["D"]:
                    self.mapGlyphs[i] = "_"
                elif sides["L"] or sides["R"]:
                    self.mapGlyphs[i] = "|"

    def whitespaceLand(self):
        for i in self.mapGlyphs:
            if self.mapGlyphs[i] == "#":
                self.mapGlyphs[i] = " "

    def placePins(self): #places 'random stuff' to empty land tiles
        if self.placeMapPins != "T":
            return
        for i in self.mapGlyphs:
            if self.mapGlyphs[i] == " " and random.randint(0,25) == 1:
                self.mapGlyphs[i] = random.choice(self.map_pins)
                if self.mapGlyphs[i] not in self.pinsInLegend:
                    self.pinsInLegend.append(self.mapGlyphs[i])
                if self.mapGlyphs[i] in ["@", "&", "+", "%", "#"]:
                    self.map_pins.remove(self.mapGlyphs[i])

    def createLegend(self):
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
        self.legend = [
            " +----------------------+",
            " |        " + Name + "        |",
            " +----------------------+",
            " |                      |"
        ]
        for p in self.pinsInLegend:
            self.legend.append(" | " + p + " = " + Meaning[p])
        for i in range(len(self.legend), self.length-1):
            self.legend.append(" |                      |")
        self.legend.append(" +----------------------+")
        self.mapGlyphs[self.width + 2] = "N"
        self.mapGlyphs[self.width*2 + 1] = "W"
        self.mapGlyphs[self.width*2 + 2] = "+"
        self.mapGlyphs[self.width*2 + 3] = "E"
        self.mapGlyphs[self.width*3 + 2] = "S"
            

def main():
    mapper = Mapper()
    config = Config()
    config.loadOptions()
    while True:
        for conf in config.menu:
            print(conf.selectIndicator)
        cmd = input(">")
        mapper.configureFromInput(cmd)
        for i in range(mapper.numberOfIslands):
            mapper.addIsland()
        print("")
        mapper.carveEdges()
        mapper.outlineIslands()
        mapper.whitespaceLand()
        mapper.placePins()
        mapper.createLegend()
        mapper.display()
        print("")

if __name__ == "__main__":
    main()
