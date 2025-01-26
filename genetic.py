from __future__ import annotations

from random import randint
from typing import List

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

    def is_movable(self, i: int):
        """A moveable is a person and has preferences"""
        return self.available and self.passengers[i] is not None

    def populate_w_sample(self, perc_available: int):
        """Populate seats (available, passengers) with data."""
        # Populate each spot with person/chair
        for i_moveable in range(self.rows * self.cols):
            if randint(1, 100) <= perc_available:  # If available
                self.available.append(True)

                if randint(1, 100) >= 50:
                    self.passengers.append(Passenger(i_moveable))  # Movable Person
                    self._n_movable_passengers += 1
                else:
                    self.passengers.append(None)  # Empty chair
                    self._n_empty += 1

            else:
                self.available.append(False)
                self.passengers.append(Passenger(i_moveable))  # Non movable person
                self._n_immovable_passengers += 1
        print(f"Added Passengers: immovable {self._n_immovable_passengers} movable {self._n_movable_passengers}")
        print(f"Empty: {self._n_empty}")

        # Add preferences for each moveable
        for i_moveable in range(self.rows * self.cols):
            # Ensure is a movable (person & preferences)
            if not self.is_movable(i_moveable):
                continue

            moveable: Passenger = self.passengers[i_moveable]

            # Add preference for people
            if randint(1, 100) <= PERC_PEOPLE_PREF:
                for _ in range(randint(1, 3)):  # Add up to 3 preferred seating next to people
                    i_rand_seat = randint(0, self.rows * self.cols - 1)

                    if (i_rand_seat == i_moveable) or (not self.is_movable(i_rand_seat)):
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
                moveable.update_pref(vert=True)
                moveable.pref_vals[1] = randint(0, self.sections - 1)

            # Add preference for aisle, middle, window
            if randint(1, 100) <= PERC_HOR_PREF:
                moveable.update_pref(hor=True)
                moveable.pref_vals[2] = randint(0, 2)

    def passenger_list(self):
        """Prints out a list of passengers"""
        for i in range(self.rows):
            for j in range(self.cols):
                index = i * self.cols + j
                if self.passengers[index] is not None:
                    print(self.passengers[index])

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


plane = Plane(6, 4, [], 3)
plane.populate_w_sample(80)
print(plane)
