#!/usr/bin/python3


import time
import random


class Life:
    def __init__(self, width, height=None):
        self.width = width
        self.height = height if height is not None else width
        self.grid = self.new_grid(self.width, self.height)

    def __str__(self):
        """
        Prints the board to console/stdout.
        """
        string = ""
        for row in self.grid:
            for cell in row:
                if cell == 0:
                    string += ". "
                elif cell == 1:
                    string += "# "
            string += "\n"
        return string

    def update(self):
        """
        Update the board state using Conway's classic rules.
        1 or fewer neighbours => death.
        2 neighbours => continuation.
        3 neights => birth or continuation.
        4 or more neighbours => death.
        """
        replacement_grid = self.new_grid(self.width, self.height)
        for row in range(self.height):
            for column in range(self.width):
                if self.neighbours(row, column) < 2:
                    replacement_grid[row][column] = 0
                elif self.neighbours(row, column) == 2:
                    replacement_grid[row][column] = self.grid[row][column]
                elif self.neighbours(row, column) == 3:
                    replacement_grid[row][column] = 1
                elif self.neighbours(row, column) > 3:
                    replacement_grid[row][column] = 0
        if self.grid == replacement_grid:
            return 0
        self.grid = replacement_grid
        return 1
    
    def new_grid(self, width, height):
        """
        Creates a grid of zeros of the specified size.
        """
        return [[0 for a in range(self.width)] for b in range(self.height)]

    def neighbours(self, row, column):
        """
        Counts the live neighbours of a particular grid position, not including itself.
        Neigbours are cells which are horizontally, vertically, or diagonally adjacent.
        """
        count = 0
        if self.grid[(row-1)%self.height][(column-1)%self.width] == 1: count += 1
        if self.grid[(row-1)%self.height][(column)%self.width] == 1: count += 1
        if self.grid[(row-1)%self.height][(column+1)%self.width] == 1: count += 1
        if self.grid[(row)%self.height][(column-1)%self.width] == 1: count += 1
        if self.grid[(row)%self.height][(column+1)%self.width] == 1: count += 1
        if self.grid[(row+1)%self.height][(column-1)%self.width] == 1: count += 1
        if self.grid[(row+1)%self.height][(column)%self.width] == 1: count += 1
        if self.grid[(row+1)%self.height][(column+1)%self.width] == 1: count += 1
        return count

    def add_glider(self):
        """
        Adds a glider pattern. This is a pattern which will move across the board
        forever unless perturbed by other cells.
        """
        row = random.randint(0, self.height)
        column = random.randint(0, self.width)
        self.grid[row%self.height][column%self.width] = 1
        self.grid[(row+1)%self.height][(column+1)%self.width] = 1
        self.grid[(row+2)%self.height][(column-1)%self.width] = 1
        self.grid[(row+2)%self.height][column%self.width] = 1
        self.grid[(row+2)%self.height][(column+1)%self.width] = 1

    def add_exploder(self):
        """
        Adds a short-lived exploder pattern.
        """
        row = random.randint(0, self.height)
        column = random.randint(0, self.width)
        self.grid[(row) % self.height][(column) % self.width] = 1
        self.grid[(row+1) % self.height][(column-1) % self.width] = 1
        self.grid[(row+1) % self.height][(column) % self.width] = 1
        self.grid[(row+1) % self.height][(column+1) % self.width] = 1
        self.grid[(row+2) % self.height][(column-1) % self.width] = 1
        self.grid[(row+2) % self.height][(column+1) % self.width] = 1
        self.grid[(row+3) % self.height][(column) % self.width] = 1

    def add_oscillator(self):
        """
        Adds an oscillating pattern. This is a pattern which repeats but does
        not move and will never stop oscillating unless perturbed by other cells.
        """
        row = random.randint(0, self.height)
        column = random.randint(0, self.width)
        self.grid[(row) % self.height][(column) % self.width] = 1
        self.grid[(row) % self.height][(column+1) % self.width] = 1
        self.grid[(row) % self.height][(column+2) % self.width] = 1

    def add_static(self):
        """
        Adds an arrangement of cells which will remain unchanged indefinitely unless
        perturbed by other cells.
        """
        row = random.randint(0, self.height)
        column = random.randint(0, self.width)
        which =  random.randint(0, 1)
        if which == 0:
            self.grid[(row) % self.height][(column) % self.width] = 1
            self.grid[(row) % self.height][(column+1) % self.width] = 1
            self.grid[(row+1) % self.height][(column) % self.width] = 1
            self.grid[(row+1) % self.height][(column+1) % self.width] = 1
        elif which == 1:
            self.grid[(row) % self.height][(column) % self.width] = 1
            self.grid[(row+1) % self.height][(column-1) % self.width] = 1
            self.grid[(row+1) % self.height][(column+1) % self.width] = 1
            self.grid[(row+2) % self.height][(column-1) % self.width] = 1
            self.grid[(row+2) % self.height][(column+1) % self.width] = 1
            self.grid[(row+3) % self.height][(column) % self.width] = 1

    @property
    def properties(self):
        return {"width": self.width, "height": self.height}


grid = Life(40, 20)

grid.add_exploder()
grid.add_exploder()
grid.add_exploder()
grid.add_glider()
grid.add_glider()
grid.add_glider()
grid.add_static()
grid.add_static()
grid.add_static()

while True:
    print(grid)
    if grid.update() == 0:
        print("Simulation ended")
        break
    time.sleep(0.1)
