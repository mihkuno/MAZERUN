import pygame
import random
import sys
import time

# ================ Global variables =================
width = 600
height = 600

stack = []
grid = []        
w = 100
isGenerated = False

current = None
target = None

# ================ Helper functions =================    
 
def removeWalls(curr, next):
   x = curr.col - next.col
   y = curr.row - next.row
   
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
   
   # draw the current 
   current.drawFocus()
   current.drawGrid()
   
   # redraw current neighbors
   for cell in current.neighbors:
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
   global w

   startX = current.col * w
   startY = current.row * w
   nextX = next.col * w
   nextY = next.row * w

   steps = 50  # number of steps to interpolate
   
   # linear interpolation function
   lerp = lambda a, b, t: a + t * (b - a)
   
   # use lerp to interpolate the movement
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
         
      # redraw the cell grid
      current.drawGrid()
      next.drawGrid()
      
      # Update the display
      pygame.display.flip()

      # Pause briefly to show the movement (you can adjust the duration)
      pygame.time.delay(1)    

   # Update the current cell
   current = next
   

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
      
   
def eventListener():
   # ==== Mouse Events ====
   # mouse_x, mouse_y = pygame.mouse.get_pos()
   
   for event in pygame.event.get():
      # ==== On Exit Event ====
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()
         
      # ==== Keyboard Events ====
      elif event.type == pygame.KEYDOWN:
         onKeyType(event)
 
     
# ================ Cell Class =======================

class Cell:
   def __init__(self, col, row):
      global w      
      self.row = row
      self.col = col
      self.x = self.col * w
      self.y = self.row * w
      
      self.visited = False
      self.walls = [True,True,True,True] # t-r-b-l
      self.neighbors = [None, None, None, None] # t-r-b-l

   
   def drawGrid(self):
      x = self.x
      y = self.y
      
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
      x = self.x
      y = self.y
      color = (239, 239, 239) 
      pygame.draw.rect(screen, color, (x, y, w, w))
         
         
   def drawFocus(self):
      x = self.x
      y = self.y
      color = (235, 77, 75)
      pygame.draw.rect(screen, color, (x, y, w, w))
      
      
   def drawTarget(self):
      x = self.x
      y = self.y
      color = (52, 216, 217)
      pygame.draw.rect(screen, color, (x, y, w, w))
      
   
   def drawFinish(self):
      x = self.x
      y = self.y
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
      
          
# ================ Create Grid ======================

def create():
   global current
   global grid
   global w
   global width
   global height
 
   # TODO: add padding to the canvas
   cols = width  // w
   rows = height // w

   # check if index is outside the grid based on rows and cols
   outbounds = lambda c, r: r<0 or c<0 or r>rows-1 or c>cols-1
   
   # get the one-dimension-grid index of cell 
   index = lambda c, r: -1 if outbounds(r,c) else c+r*rows

   # append all the cells to grid
   for row in range(rows):
      for col in range(cols):
         cell = Cell(col, row)
         grid.append(cell)

   # after creating the grid,
   for cell in grid:
      # get neighboring cell index
      tCellIx = index(cell.col,   cell.row-1)
      rCellIx = index(cell.col+1, cell.row)
      bCellIx = index(cell.col,   cell.row+1)
      lCellIx = index(cell.col-1, cell.row)
      
      # initialize cell neighbors
      if tCellIx != -1: cell.neighbors[0] = grid[tCellIx]
      if rCellIx != -1: cell.neighbors[1] = grid[rCellIx]
      if bCellIx != -1: cell.neighbors[2] = grid[bCellIx]
      if lCellIx != -1: cell.neighbors[3] = grid[lCellIx]
      
   # set first cell of grid as current visited
   current = grid[0]


# ================ Game Loop ========================

def render():
   global current
   global target
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
      generate()
               
      # Update the display
      pygame.display.flip()
      
      if isGenerated:
         break
      
      # Animate
      time.sleep(0.1)
   
   # after generated, draw the target
   if target is not None:
      target.drawTarget()
      target.drawGrid()
   
   # start game controls
   while True:
      eventListener()
      
      # Update the display
      pygame.display.flip()
      
     
if __name__ == "__main__":
   
   # ===== Pygame Setup =====
   
   # Initialize Pygame
   pygame.init()

   # Set up display
   size = (width, height) 
   screen = pygame.display.set_mode(size)
   pygame.display.set_caption("Maze Runner")

   # Load icon image
   icon_image = pygame.image.load("./public/icon.png")

   # Set icon
   pygame.display.set_icon(icon_image)
   
   # ===== Maze Game =====
   
   create() 
   render()