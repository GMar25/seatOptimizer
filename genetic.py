from random import randint

PERC_PEOPLE_PREF = 10
PERC_VERT_PREF = 10
PERC_HOR_PREF = 10

class Plane:

    """
    rows and cols defines the plane size
    perc_available is both willing to move and empty
    """
    def __init__(self, rows, cols, sections, perc_available):
        super()

        self.rows = rows
        self.cols = cols
        self.sections = sections # vertical sections

        self.available = [] # Flattened 2D array of booleans
        self.passengers = [] # Flattened 2D array of Persons
        for i in range(rows * cols):

            if (randint(1, 100) >= perc_available): # If available
                self.available.append(True)

                if (randint(1, 100) >= 2):
                    self.passengers.append(Person()) # Movable Person
                else:
                    self.passengers.append(None) # Empty chair

            else:
                self.available.append(False)
                self.passengers.append(Person()) # Non movable person

        for i in range(rows * cols):
            if self.available[i] and self.passengers[i] != None: # A movable person

                if (randint(1, 3) <= PERC_PEOPLE_PREF): 

                    add = randint(1, 5) # Number of people to add
                    while add > 0:
                        j = randint(0, rows * cols - 1)
                        if i != j and self.available[j]:
                            self.passengers[i].pref = True
                            
                            if (self.passengers[i].pref_vals[0]):
                                self.passengers[i].pref_vals[0].append(j)
                            else:
                                self.passengers[i].pref_vals[0] = [j]

                        add -= 1

                if (randint(1, 3) <= PERC_VERT_PREF):
                    self.passengers[i].vert = randint(0, self.sections - 1)

                if (randint(1, 3) <= PERC_HOR_PREF):
                    self.passengers[i].hor = randint(0, 2)         

                
    def __repr__(self):
        output = ""

        for i in range(self.rows):
            for j in range(self.cols):
                if (self.passengers[i * self.cols + j] == None):
                    output += "0 "

                elif (self.passengers[i * self.cols + j].is_movable()):
                    output += "2 "

                else:
                    output += "1 "

            output += "\n"

class Person:

    def __init__(self, people = None, vert = None, hor = None):
        super()

        self.pref = (people == None, vert == None, hor == None) # Boolean values for whether corresponding preference is set
        self.pref_vals = [people, vert, hor] # people, section vectical, section horizontal ([0, 2]: window, aisle, other)


    def is_movable(self):
        return any(self.pref)
    
    def __repr__(self):
        pass

# class genome:

#     def __init__(self):
#         super()

#         self.arr = [] # array of Persons and empty seats

#     def __init__(self, plane: Plane):
#         super()

#         self.arr = []
#         for i in range(plane.rows * plane.cols):
#             if (plane.available[i]):
#                 continue

#             else:
#                 continue


#         self.score = 0 
        
    
#     def at(self, row, col):
#         return self.arr[row * col][col]

# # def generateSeating(rows, cols, fullness):
# #     plane = Seating(rows, cols)

# #     for i in range(rows):
# #         for j in range(cols):
# #             plane.at(i, j) 

# def mate(g1, g2):


test = Plane(6, 4, 3, 80)
print(test)