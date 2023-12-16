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
w = 100
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
 
def drawCurrent():
   global current
   global target
   global previous
   
   x = current.row * w
   y = current.col * w
   color = (235, 77, 75)
   
   if current is target:
      color = (162, 155, 254) 
   
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


def lerp(a, b, t):
    return a + t * (b - a)


def refresh():
   global previous
   global current
   global target
   
   
   # optimize performance 
   # by only rendering the updated previous block
   if previous is not None:
      previous.drawBlock()
      previous.drawGrid()
   
   # assign current to previous
   previous = current
   
   # # draw the target block
   if target is not None:
      target.drawTarget()
      target.drawGrid()
   
   # draw the current block 
   current.drawFocus()
   current.drawGrid()
  
   # draw current neighbor grid
   for cell in current.neighbors:
      if cell is not None:
         cell.drawBlock()
         cell.drawGrid()
                
   # draw target neighbor grid
   if target is not None:
      for cell in target.neighbors:
         if cell is not None:
            cell.drawBlock()
            cell.drawGrid()
            

def moveUp():
    global current
    if (current.neighbors[0] is not None) and (current.walls[0] is False):
        next = current.neighbors[0]
        interpolateMovement(next)


def moveRight():
    global current
    if (current.neighbors[1] is not None) and (current.walls[1] is False):
        next = current.neighbors[1]
        interpolateMovement(next)

    
def moveDown():
    global current
    if (current.neighbors[2] is not None) and (current.walls[2] is False):
        next = current.neighbors[2]
        interpolateMovement(next)

    
def moveLeft():
    global current
    if (current.neighbors[3] is not None) and (current.walls[3] is False):
        next = current.neighbors[3]
        interpolateMovement(next)


def interpolateMovement(next):
   global current
   global previous
   global prevX
   global prevY   
   global w
      
   startX = current.row * w
   startY = current.col * w
   nextX = next.row * w
   nextY = next.col * w

   steps = 50  # number of steps for smoother interpolation   

   for step in range(steps + 1):
      
      # if not target, redraw current
      if current is not target:
         current.drawBlock()
         
      # create a new current block to interpolate next
      t = step / steps
      currentX = lerp(startX, nextX, t)
      currentY = lerp(startY, nextY, t)
      
      color = (235, 77, 75) # focus color
      pygame.draw.rect(screen, color, (currentX, currentY, w, w))    
      
      # draw the finish block on top of current
      if current is target:
         current.drawFinish()
      # draw the finish block on top of next
      elif next is target:
         next.drawFinish()
         
      # redraw the cell grid on top of the block
      current.drawGrid()
      next.drawGrid()
      
      # Update the display
      pygame.display.flip()

      # Pause briefly to show the movement (you can adjust the duration)
      pygame.time.delay(1)    

   # Update the current cell
   current = next

   # Save the final position for the next interpolation
   prevX = currentX
   prevY = currentY


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
 
     
# ================ Cell Class =======================

class Cell:
   def __init__(self, col, row):        
        self.row = row
        self.col = col
        self.walls = [True,True,True,True] # t-r-b-l
        self.visited = False

        # assign cell neighbors on create()       
        self.neighbors = [None, None, None, None] # t-r-b-l
   
   
   def drawGrid(self):
      global w
      
      x = self.row * w
      y = self.col * w
      
      # handle edge borders    
      strokeWeight = 3
      color = (10, 10, 10)
         
      # border in sides of cell
      if self.walls[0]: # tl-tr top
         pygame.draw.line(screen, color, (x,y), (x+w, y), strokeWeight)    
      
      if self.walls[1]: # tr-br right
         pygame.draw.line(screen, color, (x+w,y), (x+w, y+w), strokeWeight) 
      
      if self.walls[2]: # br-bl bottom 
         pygame.draw.line(screen, color, (x+w,y+w), (x, y+w), strokeWeight) 
      
      if self.walls[3]: # bl-tl left
         pygame.draw.line(screen, color, (x,y+w), (x, y), strokeWeight) 
         
      
   def drawBlock(self):
      global w
      
      x = self.row * w
      y = self.col * w
       
      color = (239, 239, 239) 
      pygame.draw.rect(screen, color, (x, y, w, w))
         
         
   def drawFocus(self):
      global target
      global w
      
      x = self.row * w
      y = self.col * w
      color = (235, 77, 75)
      
      if self is target:
         color = (162, 155, 254) 

      pygame.draw.rect(screen, color, (x, y, w, w))
      
      
   def drawTarget(self):
      global w

      x = self.row * w
      y = self.col * w
      color = (52, 216, 217)
      
      pygame.draw.rect(screen, color, (x, y, w, w))
      
   
   def drawFinish(self):
      global w
      
      x = self.row * w
      y = self.col * w
      color = (162, 155, 254)
      
      pygame.draw.rect(screen, color, (x, y, w, w))
      
         
   
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
   global height
   global width
   global w
   
   # Show all the cell grid and block
   for cell in grid:
      cell.drawBlock()
      cell.drawGrid()
      
   
   # maze render
   while True:      
      
      # Generate maze
      if not isGenerated:
         generate()

      refresh()
            
      # Update the display
      pygame.display.flip()
      
      if isGenerated:
         break
      
      # Animate
      # time.sleep(0.2)
   
   
   # game control
   while True:
      eventListener()
      
      # Update the display
      pygame.display.flip()
      
     
   
if __name__ == "__main__":
   setup() 
   draw()