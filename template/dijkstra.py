

# put all the created cells here to make up the grid
# row and col should start at index 0

grid = [] # Note: must be square grid based on the order of cells 
# for ex. 6 x 6 grid will have length of 36 containing Cell objects


# The Cell class is the individual box in a grid and 
# must be specified a row, column, and walls to make up the maze.
class Cell:
    def __init__(self, col, row):
        self.row = row
        self.col = col
        self.walls = [True,True,True,True] # top, right, bottom, left
        self.visited = False
        self.finish = False # only the last one in grid should be true to indicte the finish line
        
        
# Here is a sample 6 x 6 Maze Layout of the walls.
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

# get the one-dimension-grid index of cell 
def index(row, col):
    return row + (col * d)


# Create the grid of cells
# since the sample walls is 36, the grid will be 6 x 6
for row in range(d):
    for col in range(d):
        cell = Cell(col,row)
        cell.walls = walls[index(row,col)]
        grid.append(cell)
        

# =============================================================================
# The following code below should be for the maze solver
# the grid containing the cells is already created above