from __future__ import annotations

from copy import deepcopy
import heapq as hq
from random import randint, shuffle
from typing import List
import matplotlib.pyplot as plt

PERC_PEOPLE_PREF = 30
PERC_VERT_PREF = 30
PERC_HOR_PREF = 30


class Plane:
    """
    rows and cols defines the plane size
    perc_available is both willing to move and empty
    """

    def __init__(self, rows: int, cols: int, aisles: List, sections: int):
        super()

        self.rows = rows
        self.cols = cols
        self.sections = sections  # vertical sections
        self.aisles = aisles

        self.available = []  # Flattened 2D array of booleans (moveable and empty)
        self.passengers: ["Passenger" | None] = []  # Flattened 2D array of Persons or Empty seats

        # Debugging
        self._n_empty = 0
        self._n_movable_passengers = 0
        self._n_immovable_passengers = 0

    def populate_w_sample(self, perc_available: int):
        """Populate seats (available, passengers) with data."""
        # Populate each spot with person/chair
        for i_moveable in range(self.rows * self.cols):
            if randint(1, 100) <= perc_available:  # If available
                self.available.append(True)
                self.passengers.append(None)

            else:
                self.available.append(False)
                self.passengers.append(Passenger(i_moveable))  # Non movable person
                self._n_immovable_passengers += 1
        # print(f"Added Passengers: immovable {self._n_immovable_passengers} movable {self._n_movable_passengers}")
        # print(f"Empty: {self._n_empty}")

        # Add preferences for each moveable
        for i_moveable in range(self.rows * self.cols):
            # Ensure is a movable (person & preferences)
            if self.passengers[i_moveable] != None:
                continue

            if randint(1, 100) >= 50:
                self.passengers[i_moveable] = Passenger(i_moveable)  # Movable Person
                # self._n_movable_passengers += 1
            else:
                continue
                # self.passengers.append(None)  # Empty chair
                # self._n_empty += 1

            moveable: Passenger = self.passengers[i_moveable]
            # Add preference for people
            if randint(1, 100) <= PERC_PEOPLE_PREF:
                print("Adding person")
                
                for _ in range(randint(1, 3)):  # Add up to 3 preferred seating next to people
                    i_rand_seat = randint(0, self.rows * self.cols - 1)

                    if (i_rand_seat == i_moveable) or (self.passengers[i_rand_seat] == None) or (not self.passengers[i_rand_seat].is_movable()):
                        continue  # Avoid adding self or other immovable

                    # Add to each other
                    other_moveable: Passenger = self.passengers[i_rand_seat]
                    if moveable.pref_people() is None:
                        moveable.pref_vals[0] = []
                    if i_rand_seat not in moveable.pref_people():
                        moveable.pref_people().append(i_rand_seat)
                        if other_moveable.is_pref_people():  # Add pref for other people
                            other_moveable.pref_people().append(i_moveable)
                        else:
                            other_moveable.pref_vals[0] = [i_moveable]
                        other_moveable.update_pref(people=True)  # Set preference for other people

                # Set pref bc above algo may not add people
                # IE it chooses 3 locked chairs
                if moveable.pref_people() is not None:
                    moveable.update_pref(people=True)

            # Add preference for vertical
            if randint(1, 100) <= PERC_VERT_PREF:
                print("Vert pref")
                moveable.update_pref(vert=True)
                moveable.pref_vals[1] = randint(0, self.sections - 1)

            # Add preference for aisle, middle, window
            if randint(1, 100) <= PERC_HOR_PREF or (moveable.pref_vals[0] is None and moveable.pref_vals[1] is None):
                print("Hor pref")
                moveable.update_pref(hor=True)
                moveable.pref_vals[2] = randint(0, 2)

        self.passenger_list()

    def passenger_list(self):
        for i in range(self.rows):
            for j in range(self.cols):
                index = i * self.cols + j
                if self.passengers[index] is not None:
                    print(self.passengers[index])
                    
    def get_section(self, index):
        window = max(1, self.rows // 3) * self.cols

        if index < window:
            return 0

        elif index < window * 2:
            return 1

        else:
            return 2

    def get_surrounding(self, index):

        r_pos = index // self.cols
        c_pos = index % self.cols
        if (r_pos == 0): # back
            t = index + self.cols

            if (c_pos == 0):
                tr = t + 1
                mr = index + 1
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

        elif (r_pos == self.rows - 1): # front
            b = index - self.cols

            if (c_pos == 0):
                mr = index + 1
                br = b + 1
                return [b, br, mr]

            elif (c_pos == self.cols - 1):    
                ml = index - 1
                bl = b - 1
                return [b, bl, ml]

            else:
                ml = index - 1
                mr = index + 1
                bl = b - 1
                br = b + 1
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
                if self.passengers[i * self.cols + j] is None:
                    output += "0 "  # Empty Chairs
                elif not self.passengers[i * self.cols + j].is_movable():
                    output += "1 "  # Occupied, but not moveable
                else:
                    output += "2 "  # Moveable

            output += "\n"
        return output


class Passenger:
    def __init__(self, position1d: int, people=None, vert=None, hor=None):
        super()
        self.position1d = position1d
        # Boolean values for whether corresponding preference is set
        self.pref = [people is not None, vert is not None, hor is not None]
        # people, section vertical, section horizontal ([0, 2]: window, aisle, other)
        self.pref_vals = [people, vert, hor]
        self.score = -1

    def update_pref(self, people=None, vert=None, hor=None):
        """Arguments should be boolean or None"""
        if people is not None:
            self.pref[0] = people
        if vert is not None:
            self.pref[1] = vert
        if hor is not None:
            self.pref[2] = hor

    def is_pref_people(self) -> bool:
        return self.pref[0]

    def pref_people(self) -> List[int]:
        return self.pref_vals[0]

    def is_movable(self):
        return any(self.pref)

    def __repr__(self):
        return f"Passenger({self.position1d}, {self.pref}, {self.pref_vals}, {self.is_movable()})"



class Genome:

    def __init__(self, plane: Plane):
        super()

        passengers = [] # TODO slow
        for elem in plane.passengers:
            if elem != None and elem.is_movable():
                passengers.append(deepcopy(elem))

        shuffle(passengers)
        self.arr = []
        for i in range(plane.rows * plane.cols):
            if plane.passengers[i] == None or not plane.passengers[i].is_movable():
                self.arr.append(plane.passengers[i])
            else:
                self.arr.append(passengers.pop())

        self.score = -1

    def calc_heuristic(self, plane: Plane):

        r_sum = 0
        for i in range(len(self.arr)):
            p = self.arr[i]

            if p is None or not p.is_movable():
                continue

            total = 0
            met = 0

            # People
            if p.pref[0]:
                total += 1
                surrounding = plane.get_surrounding(i)

                counter = 0 # number of people met
                for elem in surrounding:
                    sp = self.arr[elem] # surrounding person
                    if sp != None and sp.position1d in p.pref_vals[0]:
                        counter += 1

                met += counter / len(p.pref_vals[0])

            # Vertical
            if p.pref[1]:
                total += 1
                if (p.pref_vals[1] == plane.get_section(i)):
                    met += 1

            # Horizontal
            if p.pref[2]:
                total += 1  
                pos = i % plane.cols
                if (p.pref_vals[2] == 0):
                    if (pos == 0 or pos == plane.cols - 1):
                        met += 1

                elif (p.pref_vals[2] == 1):
                    if (pos == plane.aisles[0] or pos == plane.aisles[0] + 1):
                        met += 1

                else:
                    if (pos != 0 and pos != plane.cols - 1 and pos != plane.aisles[0] and pos != plane.aisles[0] + 1):
                        met += 1

            p.score = met / total
            r_sum += p.score

        self.score = r_sum
        return r_sum
        
    def __repr__(self):
        output = ""

        debug_col = 4

        for i in range(len(self.arr)):
            if self.arr[i] is None:
                output += "A "  # Empty Chairs
            elif not self.arr[i].is_movable():
                output += "B "  # Occupied, but not moveable
            else:
                output += f"{self.arr[i].position1d} "  # Moveable

            if (i + 1) % debug_col == 0:
                output += '\n'

        return output

    def __lt__(self, other):
        return True


# Chair has Person attribute (use movable)
def OX(plane: Plane, g1, g2):

    # Determine cross section
    start = randint(0, plane.rows - 1) * plane.cols 
    end = randint(start / plane.cols + 1, plane.rows) * plane.cols # not inclusive

    # Create offspring and Map
    off1 = deepcopy(g1)
    used1 = set()
    empty1 = 0
    off2 = deepcopy(g2)
    used2 = set()
    empty2 = 0
    
    # Perform cross
    for i in range(start, end):
        off1.arr[i] = g2.arr[i]
        if (off1.arr[i] == None):
            empty1 += 1
        else:
            used1.add(g2.arr[i].position1d)

        off2.arr[i] = g1.arr[i]
        if (off2.arr[i] == None):
            empty2 += 1
        else:
            used2.add(g1.arr[i].position1d)

    i = 0
    j = 0
    while j < plane.rows * plane.cols:
        
        if j == start:
            j = end
            continue

        if plane.available[j]:

            while i < plane.rows * plane.cols:
                if g1.arr[i] is None:
                    if (empty1 == 0):
                        break
                    else:
                        empty1 -= 1

                elif g1.arr[i].position1d not in used1 and g1.arr[i].is_movable():
                    break

                i +=1 

            off1.arr[j] = g1.arr[i]
            i += 1
        j += 1

    i = 0
    j = 0
    while j < plane.rows * plane.cols:
        
        if j == start:
            j = end
            continue

        if plane.available[j]:

            while i < plane.rows * plane.cols:
                if g2.arr[i] is None:
                    if (empty2 == 0):
                        break
                    else:
                        empty2 -= 1

                elif g2.arr[i].position1d not in used2 and g2.arr[i].is_movable():
                    break

                i +=1 

            off2.arr[j] = g2.arr[i]
            i += 1
        j += 1

    return (off1, off2)


initial_pop = 256

plane = Plane(200, 6, [1], 3)
plane.populate_w_sample(80)

    generations = []

    curr = []
    for i in range(initial_pop):
        curr.append(Genome(plane))

iterations = 25
while iterations > 0:
    next = []

    heap = []
    for genome in curr:
        hq.heappush(heap, (-genome.calc_heuristic(plane), genome))

    for i in range(len(curr) // 2):
        elem1 = hq.heappop(heap)
        elem2 = hq.heappop(heap)

        if i == 0:
            generations.append((-elem1[0], deepcopy(elem1[1])))

        children = OX(plane, elem1[1], elem2[1])
        score1 = children[0].calc_heuristic(plane)
        score2 = children[1].calc_heuristic(plane) 

        results = []
        hq.heappush(results, (elem1[0], elem1[1]))
        hq.heappush(results, (elem2[0], elem2[1]))

        hq.heappush(results, (-score1, children[0]))
        hq.heappush(results, (-score2, children[1]))

        next.append(hq.heappop(results)[1])
        next.append(hq.heappop(results)[1])

        curr = next

    return generations[-1][1]

    # for i in range(len(generations)):
    #     print(i, generations[i][0]) 

iterations = []
scores = []
for i in range(len(generations)):
    print(i, generations[i][0]) 

iterations = []
scores = []
for i in range(len(generations)):
    iterations.append(i)
    scores.append(generations[i][0])

plt.plot(scores)
plt.title("Generation vs Max Score")
plt.xlabel("Generation")
plt.ylabel("Heurestic Score")
plt.savefig("please")

# generations, list of genomes
# genome.arr
# in that arr is a list of passengers
# passengers.score

'''
for elem in generation:

'''