
stack = []
grid = []        
cols = None
rows = None
w = 50    
isGenerated = False

# global cells
current = None
target = None

# used for control lerp
prevX = None
prevY = None

# get the one-dimension-grid index of cell 
def index(row, col):
    
    # check if index is beyond the canvas
    if (row < 0 or col < 0 or row > rows-1 or col > cols-1): 
        return -1
    
    return row + (col * cols)


def removeWalls(curr, next):
    x = curr.row - next.row
    y = curr.col - next.col
    
    if x == 1: 
        curr.walls[3] = False
        next.walls[1] = False
        
    elif x == -1:
        curr.walls[1] = False
        next.walls[3] = False
    
    if y == 1: 
        curr.walls[0] = False
        next.walls[2] = False
        
    elif y == -1:
        curr.walls[2] = False
        next.walls[0] = False


class Cell:
    def __init__(self, col, row):        
        self.row = row
        self.col = col
        self.walls = [True,True,True,True] # trbl
        self.visited = False

        # assign cell neighbors on create()       
        self.neighbors = [None, None, None, None]
    
    def block(self):
        global w
        x = self.row * w
        y = self.col * w
        
        if self.visited:
            noStroke()
            fill(250, 200)
            rect(x,y,w,w)
            
    def grid(self):
        global w
        
        x = self.row * w
        y = self.col * w
        
        noFill()
        stroke(10)
        strokeWeight(2) 

        if self.walls[0]: line(x,y,x+w,y)     # tl-tr top
        if self.walls[1]: line(x+w,y,x+w,y+w) # tr-br right
        if self.walls[2]: line(x+w,y+w,x,y+w) # br-bl bottom 
        if self.walls[3]: line(x,y+w,x,y)     # bl-tl left
                
    def getRandNeighbor(self):
        # randomly select unvisited neighbors
        selection = []
    
        for cell in self.neighbors:
            if (cell is not None) and (cell.visited is False):
                selection.append(cell)
                
        if len(selection) > 0:
            # starts at zero and up to, but not including x
            randIx   = int(random(len(selection)))
            randCell = selection[randIx]
            return randCell   
    
        return None
        
        
def create():
    global w
    global cols
    global rows
    global grid
    global current

    # TODO: add padding to the canvas
    cols = (width)  // w
    rows = (height) // w

    # append all the cells to grid
    for row in range(rows):
        for col in range(cols):
            cell = Cell(row, col);
            grid.append(cell)
    
    # after creating the grid,
    # set each cell's neighboring cell
    for cell in grid:
        tCellIx = index(cell.row,   cell.col-1)
        rCellIx = index(cell.row+1, cell.col)
        bCellIx = index(cell.row,   cell.col+1)
        lCellIx = index(cell.row-1, cell.col)
        
        if tCellIx != -1: cell.neighbors[0] = grid[tCellIx]
        if rCellIx != -1: cell.neighbors[1] = grid[rCellIx]
        if bCellIx != -1: cell.neighbors[2] = grid[bCellIx]
        if lCellIx != -1: cell.neighbors[3] = grid[lCellIx]
    
    # set first cell of grid as current visited
    current = grid[0]
            
    
def render():
    global w
    global current
    global target
    global prevX
    global prevY
    global isGenerated


    # (re)draw all the cell fill    
    for cell in grid:
        cell.block()
        
    # render current
    currX = current.row * w
    currY = current.col * w
    
    if isGenerated:
        # interpolate current movement
        if prevX is None and prevY is None:
            prevX = currX
            prevY = currY
            
        x = lerp(prevX, currX, 0.7)
        y = lerp(prevY, currY, 0.7)
    
        prevX = currX
        prevY = currY
    
    # disable if maze is generating
    else:
        x = currX
        y = currY

    noStroke()

    if current is target:
        fill(162, 155, 254) # purple
    else: fill(235, 77, 75) # red
    rect(x,y,w,w)
    
    # overlay target
    if target is not None:
        x = target.row * w
        y = target.col * w

        if current is not target:
            fill(116, 185, 255) # blue
        else: fill(162, 155, 254) # purple
        rect(x,y,w,w)

    # (re)draw all the cell wall
    for cell in grid:
        cell.grid()
    
    
def generate():
    global stack
    global grid
    global current
    global target
    global isGenerated
    
    # STEP 1: mark the current cell as visited
    current.visited = True
    
    # STEP 2
    # choose randomly one of the unvisited neighbors
    next = current.getRandNeighbor()

    if next is not None:
        # STEP 3: push the current cell to the stack
        stack.append(current)
        
        # STEP 4: remove the wall between the current and chosen cell
        removeWalls(current, next)
        
        # STEP 5: set the chosen cell as the current cell
        current = next
        
    elif len(stack) > 0:
        current = stack[-1]
        stack.pop()
        
    elif not isGenerated: # when maze is generated 
        isGenerated = True # set this to true
        
        # select random cell in grid and set as the target cell
        randIx = int(random(len(grid)))
        target = grid[randIx]
        
    else: return True
    
    
def moveTop():
    global current
    if (current.neighbors[0] is not None) and (current.walls[0] is False):
        current = current.neighbors[0]

def moveRight():
    global current
    if (current.neighbors[1] is not None) and (current.walls[1] is False):
        current = current.neighbors[1]
    
def moveBottom():
    global current
    if (current.neighbors[2] is not None) and (current.walls[2] is False):
        current = current.neighbors[2]
    
def moveLeft():
    global current
    if (current.neighbors[3] is not None) and (current.walls[3] is False):
        current = current.neighbors[3]
