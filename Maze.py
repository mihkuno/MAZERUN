
stack = []
grid = []        
cols = None
rows = None
w = 30    

# the current cell visited
current = None

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
        self.finish = False

        # assign cell neighbors on create()       
        self.neighbors = [None, None, None, None]
                
            
    def highlight(self):
        global w
        x = self.row * w
        y = self.col * w        
        noStroke()
        fill(235, 77, 75, 200)
        rect(x+6,y+6,w-11,w-11)
        
        
    def show(self):
        global w
        x = self.row * w
        y = self.col * w
        
        if self.visited:
            # put a rect on the visited cell
            noStroke()
            fill(250, 200)
            rect(x,y,w,w)
            
        
        if self.finish:
            # put a rect on the finish cell
            noStroke()
            fill(0, 210, 211, 200)
            rect(x,y,w,w)
            
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
    
    # set the last cell of the grid as target
    target = grid[-1]
    target.finish = True
    
    # set first cell of grid as current visited
    current = grid[0]
    current.visited = True
    
    
def render():
    # (re)draw all the cells
    for cell in grid:
        cell.show()
        
    # highlight current cell
    current.highlight()
    
    
def generate():
    global stack
    global grid
    global current
    
    # STEP 1
    # choose randomly one of the unvisited neighbors
    next = current.getRandNeighbor()

    if next is not None:
        # STEP 2: push the current cell to the stack
        stack.append(current)
        
        # STEP 3: remove the wall between the current and chosen cell
        removeWalls(current, next)
        
        # STEP 4: mark the chosen cell as visited and push it to the stack
        current = next
        current.visited = True
        
    elif len(stack) > 0:
        current = stack[-1]
        stack.pop()
        
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
