import random


class Percept:
    def __init__(self):
        self.wumpus = False
        self.pit = False
        self.glitter = False
        self.stench = 0
        self.breeze = False
        self.visited = False

        self.pitValue = 0
        self.wumpusValue = 0
        self.visitedValue = 0
        self.weight = 0
        self.move = 0



class World:
    def __init__(self, numberOfWumpus, numberOfArrow, numberOfPit):
        self.row = 10
        self.col = 10
        self.board = [[Percept() for j in range (self.col)] for i in range(self.row)]
        

        self.numberOfWumpus = numberOfWumpus
        self.numberOfArrow = numberOfArrow
        self.numberOfPit = numberOfPit

        self.addPit()
        self.addWumpus()
        self.addGold()
        #self.result = None
        



    def addPit(self):
        #totalPits = int((self.row * self.col) * .2)
        i = 0

        while i < self.numberOfPit:
            row = random.randint(0, self.row - 1)
            col = random.randint(0, self.col - 1)

            if row + col > 0: #avoid cell 0,0
                i += 1

                self.board[row][col].pit = True
                self.addBreeze(row, col)
            



         

    def addWumpus(self):
        #wumpus and pit can overlap
        i = 0

        while i < self.numberOfWumpus:
            row = random.randint(0, self.row - 1)
            col = random.randint(0, self.col - 1)

            if row + col > 0  : #or self.board[row][col].pit == False
                i += 1

                self.board[row][col].wumpus = True
                self.addStench(row, col)

        

    def addGold(self): #one gold
        while (True):
            row = random.randint(0, self.row - 1)
            col = random.randint(0, self.col - 1)

            if self.board[row][col].pit or self.board[row][col].wumpus:
                continue
            else:
                self.board[row][col].glitter = True
                break


    def addBreeze(self, row, col):
        if (row - 1 >= 0):
            self.board[row - 1][col].breeze = True
        if (row + 1 < self.row):
            self.board[row + 1][col].breeze = True
        if (col - 1 >= 0):
            self.board[row][col - 1].breeze = True
        if (col + 1 < self.col):
            self.board[row][col + 1].breeze = True


    def addStench(self, row, col):
        if (row - 1 >= 0):
            self.board[row - 1][col].stench += 1 #True
        if (row + 1 < self.row):
            self.board[row + 1][col].stench += 1 #True
        if (col - 1 >= 0):
            self.board[row][col - 1].stench += 1 #True
        if (col + 1 < self.col):
            self.board[row][col + 1].stench += 1 #True

    

    def show(self):
        for r in range(self.row):
            for c in range(self.col):
                print(r, c, self.board[r][c].glitter)

    