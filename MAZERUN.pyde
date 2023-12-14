
stack = []
grid = []        
cols = None
rows = None
w = 100      

# the current cell visited
current = None

# get the one-dimension-grid index of cell 
def index(row, col):
    
    # check if index is beyond the canvas
    if (row < 0 or col < 0 or row > rows-1 or col > cols-1): 
        return -1
    
    return row + (col * cols)


class Cell:
    def __init__(self, col, row):
        self.row = row
        self.col = col
        self.walls = [True,True,True,True] # trbl
        self.visited = False
        self.finish = False
            
            
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
        global grid
        
        # check if neighbor has not been visited
        neighbors = []
        
        topCellIndex    = index(self.row,   self.col-1)
        rightCellIndex  = index(self.row+1, self.col)
        bottomCellIndex = index(self.row,   self.col+1)
        leftCellIndex   = index(self.row-1, self.col)
        
        if topCellIndex != -1 and not grid[topCellIndex].visited:
            topCell = grid[topCellIndex]
            neighbors.append(topCell)
        
        if rightCellIndex != -1 and not grid[rightCellIndex].visited:
            rightCell = grid[rightCellIndex]
            neighbors.append(rightCell)
            
        if bottomCellIndex != -1 and not grid[bottomCellIndex].visited:
            bottomCell = grid[bottomCellIndex]
            neighbors.append(bottomCell)
            
        if leftCellIndex != -1 and not grid[leftCellIndex].visited:
            leftCell = grid[leftCellIndex]
            neighbors.append(leftCell)
            
        if len(neighbors) > 0:
            # starts at zero and up to, but not including x
            randNeighborIndex = int(random(len(neighbors)) )
            randNeighborCell  = neighbors[randNeighborIndex]
            return randNeighborCell   
    
        else: return None
        
        
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
        

def setup():
    global w
    global cols
    global rows
    global grid
    global current
    
    size(600, 600)
    frameRate(20)

    # TODO: add padding to the canvas
    cols = (width)  // w
    rows = (height) // w

    # append all the cells to grid
    for row in range(rows):
        for col in range(cols):
            cell = Cell(row, col);
            grid.append(cell)
    
    # set the last cell of the grid as target
    target = grid[-1]
    target.finish = True
    
    # set first cell of grid as current visited
    current = grid[0]
    current.visited = True
       
done = False
def draw():
    global stack
    global grid
    global current
    global done
    
    background(200)
    
    # show all the cells
    for cell in grid:
        cell.show()
        
    current.highlight()
    
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
        
    elif done == False:
        done = True
        for i in grid: 
            print(i.walls)
