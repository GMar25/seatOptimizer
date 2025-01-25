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




    