import pygame
import random
import sys
import time

# ================ Global variables ================
width = 600
height = 600

stack = []
grid = []        
cols = None
rows = None
w = 50
isGenerated = False

# global cells
current = None
target = None
previous = None

# used for control lerp
prevX = None
prevY = None


# ================ Init functions ==================

# Initialize Pygame
pygame.init()

# Set up display
size = (width, height) 
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze Runner")

# in order to get the window size
# width, height = pygame.display.get_window_size()

# Load icon image
icon_image = pygame.image.load("./public/icon.png")

# Set icon
pygame.display.set_icon(icon_image)


# ================ Helper functions =================

def moveUp():
    global current
    if (current.neighbors[0] is not None) and (current.walls[0] is False):
        current = current.neighbors[0]


def moveRight():
    global current
    if (current.neighbors[1] is not None) and (current.walls[1] is False):
        current = current.neighbors[1]

    
def moveDown():
    global current
    if (current.neighbors[2] is not None) and (current.walls[2] is False):
        current = current.neighbors[2]

    
def moveLeft():
    global current
    if (current.neighbors[3] is not None) and (current.walls[3] is False):
        current = current.neighbors[3]


def onKeyType(event):
   global isGenerated
   # if esc pressed, close program
   if event.key == pygame.K_ESCAPE:
      pygame.quit()
      sys.exit()
   
   if isGenerated:
      if event.key == pygame.K_UP:      moveUp()
      elif event.key == pygame.K_DOWN:  moveDown()
      elif event.key == pygame.K_LEFT:  moveLeft()
      elif event.key == pygame.K_RIGHT: moveRight()
   
   else: 
      print("Key Pressed:", pygame.key.name(event.key))
      

def onExit():
   pygame.quit()
   sys.exit()
   
   
def eventListener():
   # ==== Mouse Events ====
   # mouse_x, mouse_y = pygame.mouse.get_pos()
   
   for event in pygame.event.get():
      # ==== On Exit Event ====
      if event.type == pygame.QUIT:
         onExit()
         
      # ==== Keyboard Events ====
      elif event.type == pygame.KEYDOWN:
         onKeyType(event)


def index(row, col): # get the one-dimension-grid index of cell 
    # check if index is beyond the canvas
    if (row < 0 or col < 0 or row > rows-1 or col > cols-1): 
        return -1
    
    return row + (col * cols)
 
 
def drawCurrent():
   global current
   global target
   
   x = current.row * w
   y = current.col * w
   color = (235, 77, 75)
   
   if current is target:
      color = (162, 155, 254) 
   
   pygame.draw.rect(screen, color, (x, y, w, w))


def drawTarget():
   global target
   x = target.row * w
   y = target.col * w
   color = (52, 216, 217)
   
   pygame.draw.rect(screen, color, (x, y, w, w))
 
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
        length = len(grid) - 1
        randIx = random.randint(0, length)
        target = grid[randIx]


# ================ Cell Class =======================

class Cell:
   def __init__(self, col, row):        
        self.row = row
        self.col = col
        self.walls = [True,True,True,True] # trbl
        self.visited = False

        # assign cell neighbors on create()       
        self.neighbors = [None, None, None, None]
   
   
   def getRandNeighbor(self):
      # randomly select unvisited neighbors
      selection = []
   
      for cell in self.neighbors:
         if (cell is not None) and (cell.visited is False):
            selection.append(cell)
                
      if len(selection) > 0:
         length = len(selection) - 1
         randIx = random.randint(0, length)
         randCell = selection[randIx]
         return randCell   
    
      return None
   
   
   def drawBlock(self):
      global width, height
      global w, screen
      
      x = self.row * w
      y = self.col * w
      color = (200, 200, 200)

      if self.visited:
         color = (239, 239, 239) 
      
      pygame.draw.rect(screen, color, (x, y, width, height))
   
   
   def drawGrid(self):
      global w, screen
      strokeWeight = 3
      x = self.row * w
      y = self.col * w
      color = (10, 10, 10)
   
      if self.walls[0]: # tl-tr top
         pygame.draw.line(screen, color, (x,y), (x+w, y),     strokeWeight)     
      
      if self.walls[1]: # tr-br right
         pygame.draw.line(screen, color, (x+w,y), (x+w, y+w), strokeWeight) 
      
      if self.walls[2]: # br-bl bottom 
         pygame.draw.line(screen, color, (x+w,y+w), (x, y+w), strokeWeight) 
      
      if self.walls[3]: # bl-tl left
         pygame.draw.line(screen, color, (x,y+w), (x, y),     strokeWeight)     
      
          
# ================ Create Maze Grid ==================

def setup():
   global current
   global grid
   global w
   global cols
   global rows
   global width
   global height
   
   # TODO: add padding to the canvas
   cols = width  // w
   rows = height // w

   # append all the cells to grid
   for row in range(rows):
      for col in range(cols):
         cell = Cell(row, col);
         grid.append(cell)

   # after creating the grid,
   for cell in grid:
      # get neighboring cell index of current
      tCellIx = index(cell.row,   cell.col-1)
      rCellIx = index(cell.row+1, cell.col)
      bCellIx = index(cell.row,   cell.col+1)
      lCellIx = index(cell.row-1, cell.col)
      
      # set current cell's neighboring cell
      if tCellIx != -1: cell.neighbors[0] = grid[tCellIx]
      if rCellIx != -1: cell.neighbors[1] = grid[rCellIx]
      if bCellIx != -1: cell.neighbors[2] = grid[bCellIx]
      if lCellIx != -1: cell.neighbors[3] = grid[lCellIx]

   # set first cell of grid as current visited
   current = grid[0]


# ================ Game Loop ========================

def draw():
   global current
   global target
   global previous
   global grid
   global isGenerated
   
   while True:
      eventListener()

      # Clear the screen
      color = (255, 255, 255)
      screen.fill(color)

      # Show all the cell blocks
      for cell in grid:
         cell.drawBlock()
         
      # Show target cell
      if target is not None:
         drawTarget()
         
      # Show current cell
      drawCurrent()
      
      # Show all the cell grid
      for cell in grid:
         cell.drawGrid()
         
      # Generate maze
      if not isGenerated:
         generate()

      # Update the display
      pygame.display.flip()
      
      # Animate
      # time.sleep(0.7)
      
   
if __name__ == "__main__":
   setup() 
   draw()