#!/usr/bin/env python3

"""
    A simple sketch for a Mars Rover problem.
"""

def main(input):
    lines = [s.strip() for s in input.splitlines() if s.strip()] #Strip here just to make formatting the sample easier. Remove if whitespace or blank lines in instructions matter.
    # Initialising the plateau
    plat_info = lines[0].split()
    # Global plateau info. Ideally these should actually be based on rover sensors.
    global plateau, min_x, min_y, max_x, max_y
    min_x = 0
    min_y = 0
    max_x = int(plat_info[0])
    max_y = int(plat_info[1])
    plateau = dict() # For collision detection. {pos: rover}

    # Initialising the rover start positions and their instructions
    rovers = []
    for i in range(1, len(lines[1:]), 2):
        (x, y, d) = lines[i].split()
        (x, y) = (int(x), int(y))
        r = Rover(x, y, d, lines[i+1])
        #print(f"Rover {i}: {(r.x, r.y, r.orientation, r.instructions)}")
        rovers.append(r)
        plateau[(r.x, r.y)] = r

    # Executing rover instructions
    for r in rovers:
        r.execute_instructions()
        #print(f"{r}: {x1, y1, d1}")

    # The output should be each rover's final coordinates and heading
    return "\n".join(f"{r.x} {r.y} {r.orientation}" for r in rovers)

def _sample_inp():
    return """
        5 5
        1 2 N
        LMLMLMLMM
        3 3 E
        MMRMMRMRRM
    """

def _colliding_inp():
    return """
        5 5
        1 2 N
        LMLMLMLMM
        3 3 E
        MMRMMRMRRM
        5 5 S
        MMMMM
    """

def _out_of_bounds_inp():
    return """
        5 5
        1 2 N
        LMLMLMLMM
        3 3 E
        MMRMMRMRRM
        5 5 S
        LM
    """

class Rover:
    directions = ["N", "E", "S", "W"]
    offsets = {
        "N": (0, 1),
        "E": (1, 0),
        "S": (0, -1),
        "W": (-1, 0)
    }

    def __init__(self, x, y, orientation, instructions=""):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.instructions = instructions

    def get_pos(self):
        return (self.x, self.y, self.orientation)

    def execute_instructions(self):
        for command in self.instructions:
            # if-elif chain here since python doesn't have switch-statements or case expressions until version 3.10
            if command == "L":
                self.rotate_left()
            elif command == "R":
                self.rotate_right()
            elif command == "M":
                self.move_forwards()
            else:
                raise Exception(f"Rover does not know how to execute {command}")

    def rotate_right(self):
        i = Rover.directions.index(self.orientation)
        l = len(Rover.directions)
        self.orientation = Rover.directions[(i + 1) % l]

    def rotate_left(self):
        i = Rover.directions.index(self.orientation)
        l = len(Rover.directions)
        self.orientation = Rover.directions[(i - 1 + l) % l]

    def move_forwards(self):
        (off_x, off_y) = Rover.offsets[self.orientation]
        (x1, y1) = (self.x + off_x, self.y + off_y)
        #print(f"Moving {self.orientation} from {self.x, self.y} to {x1, y1}")
        if self.valid_move(x1, y1):
            #update the global plateau info
            global plateau
            plateau[(x1, y1)] = plateau.pop((self.x, self.y))
            (self.x, self.y) = (x1, y1)
        else:
            raise Exception(f"Rover {self} tried to move to {x1, y1}, which is an invalid move")

    def valid_move(self, x1, y1):
        # Checks if the intended move is valid. New pos should be:
        # -  In the plateau's bounds
        # -  Doesn't collide with another rover
        # Note: plateau info here is global, since ideally the collision detection would be based on the rover's onboard sensors.
        global plateau
        # In plateau bounds?
        if x1 < min_x or x1 > max_x or y1 < min_y or y1 > max_y:
            return False
        # Collides with another rover?
        r = plateau.get((x1, y1), None)
        if r is not None:
            return False
        return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        inp = "\n".join(sys.argv[1:])
        print("Running plateau problem on input:")
        print(inp)
        print("---- Output: -----")
        print(main(inp))
    else:
        print("Sample task:")
        #print("----")
        output = main(_sample_inp())
        #output = main(_colliding_inp())
        #output = main(_out_of_bounds_inp())
        print("---- Output: ----")
        print(output)
