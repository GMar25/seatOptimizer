from random import randint

class Plane:

    def __init__(self, rows, cols):
        super()

        self.rows = rows
        self.cols = cols


class Person:

    def __init__(self):
        super()

        self.id = 0 
        self.seat = (0, 0) # Row, column (0, 0 is front left)

        self.pref = \
            [
                (0, []), # bool, people
                (0, 0),  # bool, section vertical 
                (0, 0),  # bool, section horizontal [0, 2]: window, aisle, other
            ] 


class Seating:

    def __init__(self):
        super()

        self.arr = [] # array of Persons
        self.score = 0 # heurestic result

    def __init__(self, rows, cols, fullness):
        super()


        self.arr = []
        for i in range(rows * cols):
            if (randint(1, 100) <= fullness):
                self.arr.append(Person())

            else:


        self.score = 0
        
    
    def at(self, row, col):
        return self.arr[row * col][col]

def generateSeating(rows, cols, fullness):
    plane = Seating(rows, cols)

    for i in range(rows):
        for j in range(cols):
            plane.at(i, j) 

