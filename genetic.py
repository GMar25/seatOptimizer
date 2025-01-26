from random import randint

PERC_PEOPLE_PREF = 10
PERC_VERT_PREF = 10
PERC_HOR_PREF = 10

class Plane:

    """
    rows and cols defines the plane size
    perc_available is both willing to move and empty
    """
    def __init__(self, rows, cols, perc_available, aisle):
        super()

        self.rows = rows
        self.cols = cols
        self.aisle = aisle

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
                            self.passengers[i].pref[0] = True
                            
                            if (self.passengers[i].pref_vals[0]):
                                self.passengers[i].pref_vals[0].append(j)
                            else:
                                self.passengers[i].pref_vals[0] = [j]

                        add -= 1

                if (randint(1, 3) <= PERC_VERT_PREF):
                    self.passengers[i].pref[1] = True
                    self.passengers[i].pref_vals[1] = randint(0, self.sections - 1)

                if (randint(1, 3) <= PERC_HOR_PREF):
                    self.passengers[i].pref[2] = True
                    self.passengers[i].pref_vals[2] = randint(0, 2)         

    def get_section(self, index):
        index /= self.cols
        window = index / 3

        if index < window:
            return 0

        elif index < window * 2:
            return 1

        else:
            return 2

    def get_surrounding(self, index):
        indices = []

        r_pos = index / self.cols
        c_pos = index % self.cols
        if (r_pos == 0): # front
            t = index + self.cols

            if (c_pos == 0):
                tr = t + 1
                mr = index - 1
                return [t, tr, mr]

            elif (c_pos == self.cols - 1):    
                tl = t - 1
                ml = index - 1
                return [t, tl, ml]

            else:
                tl = t - 1
                tr = t + 1
                ml = index - 1
                mr = index + 1
                return [t, tl, tr, ml, mr]

        elif (r_pos == self.rows - 1): # back
            b = index - self.cols

            if (c_pos == 0):
                mr = index + 1
                br = b + 1
                return [b, br, mr]

            elif (c_pos == self.cols - 1):    
                ml = index - 1
                bl = index - 1
                return [b, bl, ml]

            else:
                ml = index - 1
                mr = index + 1
                bl = t - 1
                br = t + 1
                return [b, bl, br, ml, mr]

        else:
            t = index + self.cols
            b = index - self.cols

            if (c_pos == 0):
                tr = t + 1
                mr = index + 1
                br = b + 1
                return [t, tr, b, br, mr]

            elif (c_pos == self.cols - 1):    
                tl = t - 1
                ml = index - 1
                bl = b - 1
                return [t, tl, b, bl, ml]

            else:
                tr = t + 1
                mr = index + 1
                br = b + 1
                tl = t - 1
                ml = index - 1
                bl = b - 1
                return [t, tl, tr, ml, mr, b, bl, br]

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

        self.pos = 0
        self.pref = (people == None, vert == None, hor == None) # Boolean values for whether corresponding preference is set
        self.pref_vals = [people, vert, hor] # people, section vectical, section horizontal ([0, 2]: window, aisle, other)
        self.happiness = 0

    def is_movable(self):
        return any(self.pref)
    
    def __repr__(self):
        pass


class Genome:

    def __init__(self):
        super()

        self.arr = [] # array of Persons and empty seats
        self.score = -1

    def __init__(self, plane: Plane):
        super()

        self.arr = []
        for i in range(plane.rows * plane.cols):
            self.arr[i].append(Person())
        self.score = -1

    def __init__(self, g):
        super()

        self.arr = list(g.arr())
        self.score = -1

    def calc_heuristic(self, plane: Plane):

        r_sum = 0
        for i in range(len(self.arr)):
            p = self.arr[i]
            total = 0
            met = 0

            # People
            if p.pref[0]:
                total += 1
                surrounding = plane.get_surrounding()

                counter = 0 # number of people met
                for elem in surrounding:
                    sp = self.arr[elem] # surrounding person
                    if sp.pos in p.pref_vals[0]:
                        counter += 1

                met += counter / len(p.pref_vals[0])

            # Vertical
            if p.pref[1]:
                total += 1
                if (p.pref_val[1] == plane.get_section(i)):
                    met += 1

            # Horizontal
            if p.pref[2]:
                total += 1  
                pos = i % p.cols
                if (p.pref_vals[2] == 0):
                    if (pos == 0 or pos == plane.cols - 1))
                        met += 1

                elif (p.pref_vals[2] == 1):
                    if (pos == plane.aisle[0] or pos == plane.aisle[0] + 1):
                        met += 1

                else:
                    if (pos != 0 and pos != plane.cols - 1 and pos != plane.aisle[0] and pos != plane.aisle[0] + 1):
                        met += 1

            p.score = met / total # TODO
            r_sum += p.score
        
    

# Chair has Person attribute (use movable)
def OX(plane: Plane, g1, g2):

    # Determine cross section
    start = randint(0, len(plane.rows) - 1) * plane.cols 
    end = randint(start + 1, len(plane.rows) - 1) * plane.cols

    # Create offspring and Map
    off1 = Genome(g1)
    used1 = set()
    off2 = Genome(g2)
    used2 = set()
    
    # Perform cross
    for i in range(start, end):
        off1.arr[i] = g2.arr[i]
        used1.add(off1.arr[i])

        off2.arr[i] = g1.arr[i]
        used2.add(off2.arr[i])

    # Move remaining elements
    order = OX_helper(g1, used1)
    i = 0
    for j in range(0, plane.rows * plane.cols):
        if plane.available[j]:
            off1.arr[j] = order[i]
            i += 1

    order = OX_helper(g2, used2)
    i = 0
    for j in range(0, plane.rows * plane.cols):
        if plane.available[j]:
            off2.arr[j] = order[i]
            i += 1

    return (off1, off2)

def OX_helper(g, used):
    order = []


    for i in range(len(g.arr)):
        if g.arr[i].is_movable() and i not in used:
            order.append(i)

    return order

