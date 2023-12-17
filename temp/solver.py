

# put all the created cells here to make up the grid
# row and col should start at index 0

grid = [] # Note: must be square grid based on the order of cells 
# for ex. 6 x 6 grid will have length of 36 containing Cell objects


# The Cell class is the individual box in a grid and 
# must be specified a column, row, and walls to make up the maze.
class Cell:
   def __init__(self, col, row):
      self.col = col     
      self.row = row
      self.walls = [True,True,True,True] # t-r-b-l
      self.neighbors = [None, None, None, None] # t-r-b-l

        
# Here is the template 6 x 6 Maze Wall layout.
walls = [
   [True, True, False, True],
   [True, False, True, True],
   [True, False, True, False],
   [True, False, False, False],
   [True, False, True, False],
   [True, True, True, False],
   [False, False, True, True],
   [True, False, True, False],
   [True, True, False, False],
   [False, False, False, True],
   [True, False, True, False],
   [True, True, False, False],
   [True, True, False, True],
   [True, False, False, True],
   [False, True, True, False],
   [False, True, False, True],
   [True, False, False, True],
   [False, True, True, False],
   [False, False, False, True],
   [False, True, True, False],
   [True, False, True, True],
   [False, True, False, False],
   [False, False, True, True],
   [True, True, False, False],
   [False, False, True, True],
   [True, False, True, False],
   [True, True, False, False],
   [False, True, True, True],
   [True, False, False, True],
   [False, True, False, False],
   [True, False, True, True],
   [True, False, True, False],
   [False, False, True, False],
   [True, False, True, False],
   [False, True, True, False],
   [False, True, True, True],
]

d = 6 # dimension of the grid

# check if index is outside the grid based on rows and cols
outbounds = lambda c, r: r<0 or c<0 or r>d-1 or c>d-1

# get the one-dimension-grid index of cell 
index = lambda c, r: -1 if outbounds(r,c) else c+r*d

# create and append all cells to grid
# since the sample walls is 36, the grid will be 6 x 6
for row in range(d):
    for col in range(d):
        cell = Cell(col, row)
        grid.append(cell)


# =============================================================================
# Goal: find the path to the target 
# using dijkstra or A* algorithm

# The following code below should be for the maze solver
# the grid containing the cells is already created above

# the last cell in the grid is the target
target = grid[-1]

# the current cell is the first cell in the grid
current = grid[0]

# the stack is used to store the cells 
# which backtraces a path to the target
stack = []