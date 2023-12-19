import pygame
import random
import time
import sys
import heapq

# ================ Global variables =================

# ==== configure in main.py ====
xOffset = 0
yOffset = 0
level = 0
area = 0
screen = None
sound_move = None
sound_target = None
sound_wall = None
sound_clear = None
sound_trail = None

# ====== private variables ======
stack = []
grid  = []        
searched = []

isAllowControl = False

current = None
target = []
finish = []
alreadyFinish = []


# ======= level variables =======
w = 0 # cell width
targetLimit = None


# ================ Control functions =================    

def moveSound(next=None):
   global target
   global finish
   global sound_move
   global sound_target

   if next in finish and finish is not None:
      sound_move.play()
   elif next is None:
      sound_wall.play()
   elif next in target:
      sound_target.play()
   else:
      sound_move.play()
      
   
def moveUp():
   global current
   if (current.neighbors[0] is not None) and (current.walls[0] is False):
      next = current.neighbors[0]
      moveSound(next)
      interpolateMovement(next)
   else:
      moveSound()


def moveRight():
   global current
   if (current.neighbors[1] is not None) and (current.walls[1] is False):
      next = current.neighbors[1]
      moveSound(next)
      interpolateMovement(next)
   else:
      moveSound()
    
    
def moveDown():
   global current
   if (current.neighbors[2] is not None) and (current.walls[2] is False):
      next = current.neighbors[2]
      moveSound(next)
      interpolateMovement(next)
   else:
      moveSound()
         
    
def moveLeft():
   global current
   if (current.neighbors[3] is not None) and (current.walls[3] is False):
      next = current.neighbors[3]
      moveSound(next)
      interpolateMovement(next)
   else:
      moveSound()
      

def interpolateMovement(next):
   global current
   global alreadyFinish
   global target
   global finish

   startX = current.x
   startY = current.y
   nextX = next.x
   nextY = next.y

   steps = 25  # number of steps to interpolate
   
   # linear interpolation function
   lerp = lambda a, b, t: a + t * (b - a)
   
   # use lerp to interpolate the movement
   for step in range(steps + 1):
      
      # if not target, redraw current
      if current not in target:
         current.drawVisit()
      
      elif current in finish and alreadyFinish:
         current.drawFinish()
         
                  
      # create a new current block to interpolate next
      t = step / steps
      currentX = lerp(startX, nextX, t)
      currentY = lerp(startY, nextY, t)
      
      color = (235, 77, 75) # focus color
      pygame.draw.rect(screen, color, (currentX, currentY, w, w))    
      
      
      if current in finish and current not in alreadyFinish:
         current.drawFinish()
 
      # draw the finish block on top of next
      elif current in target and current not in finish:
         current.drawFinish()
 
      # draw the finish block on top of next
      elif next in target and next not in finish:
         next.drawFinish()
            
      # redraw the cell grid
      current.drawGrid()
      next.drawGrid()
      
      # Update the display
      pygame.display.flip()

      # Pause briefly to show the movement (you can adjust the duration)
      pygame.time.delay(1)    

   
   if next in target and next not in finish:
      finish.append(next) 
   
   elif next in target and next in finish:
      alreadyFinish.append(next)
      
   # Update the current cell
   current = next

      
def eventListener():   
   global current
   global target
   global isAllowControl
   
   for event in pygame.event.get():
      
      # ==== Exit Event ====
      if event.type == pygame.QUIT:
         pygame.quit()
         sys.exit()
         
      elif event.type == pygame.KEYDOWN:
         # esc pressed, close program
         if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
         
      # == Game Controls ==
      if isAllowControl: 
         
         # move the current cell
         if event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_UP:      moveUp()
            elif event.key == pygame.K_DOWN:  moveDown()
            elif event.key == pygame.K_LEFT:  moveLeft()
            elif event.key == pygame.K_RIGHT: moveRight()
         
         # hover the target cells
         for t in target:
            if t and t.block.collidepoint(pygame.mouse.get_pos()):
               pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
               # on target click, solve the target cell
               if event.type == pygame.MOUSEBUTTONDOWN:
                  pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                  solve(current, t)
               break
            else: pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
  
  
# ============== Min-Heap CellNode Class ===============

class CellNode:
   def __init__(self, col, row):
      global w      
      global xOffset
      global yOffset
      
      # == cell attributes ==
      self.row = row
      self.col = col
      self.x   = self.col * w + xOffset
      self.y   = self.row * w + yOffset
      self.w   = w
      
      self.block     = None
      self.visited   = False
      self.walls     = [True,True,True,True] # t-r-b-l
      self.neighbors = [None, None, None, None] # t-r-b-l
      
      # == node attributes ==
      self.distance = float('inf')
      self.predecessor = None


   # less than operator for class instances
   def __lt__(self, other): 
      return self.distance < other.distance

      
   def drawGrid(self):
      x = self.x
      y = self.y
      w  = self.w
      
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
         
         
   def drawVisit(self):
      color = (239, 239, 239) 
      self.block = pygame.Rect((self.x, self.y, self.w, self.w))
      pygame.draw.rect(screen, color, self.block)
      
   
   def drawTrail(self):
      color = (247, 215, 148)
      self.block = pygame.Rect((self.x, self.y, self.w, self.w))
      pygame.draw.rect(screen, color, self.block)
      
      
   def drawSearch(self):
      color = (178, 190, 195)
      self.block = pygame.Rect((self.x, self.y, self.w, self.w))
      pygame.draw.rect(screen, color, self.block)  
            
            
   def drawBlock(self):
      color = (99, 110, 114)
      self.block = pygame.Rect((self.x, self.y, self.w, self.w))
      pygame.draw.rect(screen, color, self.block)
        
         
   def drawActive(self):
      color = (237, 76, 103)
      self.block = pygame.Rect((self.x, self.y, self.w, self.w))
      pygame.draw.rect(screen, color, self.block)
      
      
   def drawFocus(self):
      color = (76, 209, 55)
      self.block = pygame.Rect((self.x, self.y, self.w, self.w))
      pygame.draw.rect(screen, color, self.block)
      
      
   def drawTarget(self):
      color = (116, 185, 255)
      self.block = pygame.Rect((self.x, self.y, self.w, self.w))
      pygame.draw.rect(screen, color, self.block)
      
   
   def drawFinish(self):
      color = (162, 155, 254)
      self.block = pygame.Rect((self.x, self.y, self.w, self.w))
      pygame.draw.rect(screen, color, self.block)
      
         
   def getRandomNeighbor(self):
      # randomly select unvisited neighbors
      selection = []
   
      for cell in self.neighbors:
         if (cell is not None) and (cell.visited is False):
            selection.append(cell)
                
      if len(selection) > 0:
         randIx = random.randint(0, len(selection)-1)
         randCell = selection[randIx]
         return randCell   
    
      return None   
   
   
   def hasWallBetween(self, other):
      x = self.col - other.col
      y = self.row - other.row
      
      if y ==  1: return self.walls[0]
      if y == -1: return self.walls[2]
      if x == -1: return self.walls[1]
      if x ==  1: return self.walls[3]
      return False
   
   
   def removeWallBetween(self, other):
      x = self.col - other.col
      y = self.row - other.row
      
      if x == 1: 
         self.walls[3] = False
         other.walls[1] = False
         
      elif x == -1:
         self.walls[1] = False
         other.walls[3] = False
      
      if y == 1: 
         self.walls[0] = False
         other.walls[2] = False
         
      elif y == -1:
         self.walls[2] = False
         other.walls[0] = False
      
      sound_clear.play()
         
 
# ================== Generate Grid ===================    

def generate():
   global stack
   global grid
   global current
   global target
   global targetLimit
   global isAllowControl
   
   # prevent user from controlling the maze
   isAllowControl = False
   
   # get random cell in grid as starting point
   cell = grid[random.randint(0, len(grid)-1)]
   
   # refresh the cell and its previous
   # and their neighboring cells on the grid
   def refresh(next):
      nonlocal cell
      cell.drawVisit()
      cell.drawGrid()
      
      for n in cell.neighbors:
         if n is not None and not n.visited:
            n.drawBlock()
            n.drawGrid()
            
      cell = next
      
      for n in cell.neighbors:
         if n is not None and not n.visited:
            n.drawSearch()
            n.drawGrid()
            
      cell.drawFocus()
      cell.drawGrid()      
      
      # update the display
      pygame.display.flip()
      
      # animate
      # time.sleep(0.05)

   while True:
      # fix window freeze
      eventListener()
            
      # STEP 1: mark the current cell as visited
      cell.visited = True
      
      # STEP 2A:
      # choose randomly one of the unvisited neighbors
      next = cell.getRandomNeighbor()

      if next is not None:
         # STEP 3: push the current cell to the stack
         stack.append(cell)
         
         # STEP 4: remove the wall between the current and chosen cell
         cell.removeWallBetween(next)
         
         # STEP 5: set the chosen cell as the current cell
         refresh(next)
         
      # STEP 2B:
      # if no neighbors, pop a cell from the stack 
      # and make it the current cell
      elif len(stack) > 0:
         next = stack[-1]
         stack.pop()
         
         # STEP 5: set the chosen cell as the current cell
         refresh(next)
         
      elif not isAllowControl: # when maze is generated 
         # create count of targetLimit unique random numbers list
         unique = random.sample(range(0, len(grid)), 3)

         # create target cell list
         for u in unique:
            target.append(grid[u])
         
         # allow user controls
         isAllowControl = True 
         
         # generate is complete
         break
   
   # clear initial cell
   cell.drawVisit()
   cell.drawGrid()
   
   # show current cell
   current.drawActive()
   current.drawGrid()      
      
   # update the display
   pygame.display.flip()
      
   # allow user controls
   isAllowControl = True


# ================ Create Grid ======================

def create():
   global current
   global grid
   global area

   cols = area // w
   rows = area // w

   # check if index is outside the grid based on rows and cols
   outbounds = lambda c, r: r<0 or c<0 or r>rows-1 or c>cols-1
   
   # get the one-dimension-grid index of cell 
   index = lambda c, r: -1 if outbounds(r,c) else c+r*rows

   # append all the cells to grid
   for row in range(rows):
      for col in range(cols):
         cell = CellNode(col, row)
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
      
   # set middle cell of grid as current visited
   current = grid[index(cols//2, rows//2)]
   

# ================ Game Loop ========================

def render():
   global current
   global target
   global grid
   global isAllowControl
   global w
   
   # show all the cell grid and block
   for cell in grid:
      cell.drawBlock()
      cell.drawGrid()
    
   # generate maze
   generate()
   
   # after generated, draw the target
   if target is not None:
      for t in target:
         t.drawTarget()
         t.drawGrid()
      
   # set up the framerate clock
   clock = pygame.time.Clock()
   
   # start game controls
   while True:
      eventListener()
      
      # Update the display
      pygame.display.flip()
      
      # Cap the frame rate
      clock.tick(60)


# =============== Dijkstra Solver ====================

def solve(start, end):
   global grid
   global searched
   global target
   global finish
   global isAllowControl

   # prevent user from controlling the maze
   isAllowControl = False
   
   # disktra can solve all short paths to all targets at once from the start position
   # the problem is that when start moves, the distance and predecessor of all cells 
   # is still pointing from the original position from when the search was started.  
   # so we need to reset the distance and predecessor of all cells
   # because the new position has a new path to the target

   # reset previous searched cells   
   for cell in searched:
      cell.distance = float('inf')
      cell.predecessor = None
      
      if (
         cell is not start and 
         cell is not end and
         cell not in target and
         cell not in finish
      ):
         cell.drawVisit()
         cell.drawGrid()   
   
   previous = None
   isSolved = False
   searched = []
   queue = []
   path = []
   
   # the start distance is 0
   start.distance = 0
   start.predecessor = None

   # create a priority queue and add the start node
   heapq.heappush(queue, (start.distance, start))
   
   # start the first cell searched
   # since it is pushed to the queue
   start.drawSearch()
   start.drawGrid()
      
   # start the search algorithm
   while queue:
      if isSolved: break      
      
      # fix window freeze
      eventListener()         
      
      # get the node with the smallest distance
      distance, cell = heapq.heappop(queue)
      
      # check next neighbor
      for neighbor in cell.neighbors:
         if neighbor and not neighbor.hasWallBetween(cell):
            
            # used later to reset searched cells
            searched.append(neighbor)
            
            # calculate the distance to the neighbor
            distance = distance + 1
            
            # update the distance if necessary
            if distance < neighbor.distance:
               neighbor.distance = distance
               neighbor.predecessor = cell
               
               # add the neighbor to the queue
               heapq.heappush(queue, (neighbor.distance, neighbor))
      
               # draw the search
               if neighbor is not end:
                  neighbor.drawFocus()
                  neighbor.drawGrid()
               else:
                  # check if reached the end
                  isSolved = True
                  break
               # remove focus of previous cell
               if previous is not None:
                  previous.drawSearch()
                  previous.drawGrid()
               previous = neighbor
               
               # play move sound
               sound_move.play()
               # then update display
               pygame.display.flip()
               # animate
               time.sleep(0.05)
               
   # remove focus of previous cell
   if previous is not None:
      previous.drawSearch()
      previous.drawGrid()
      
   # while trail is being drawn,
   # teleport focus to start position
   start.drawActive()
   start.drawGrid()

   # == reconstruct the shortest path ==
                 # begin from end node
   cell = end # backtrace to start node
   # while loop to trace back to the start
   while cell:
      path.append(cell)
      cell = cell.predecessor
   # its constructed backwards, 
   path.reverse() # so reverse it
   
   # == draw the shortest path ==
   for cell in path:
      # fix window freeze
      eventListener()
      
      if (
         cell is not start and 
         cell is not target
      ):
         cell.drawTrail()
         cell.drawGrid()

      # then update display
      pygame.display.flip()
      # play trail sound
      sound_trail.play()
      # animate
      time.sleep(0.08)   
   
   # reset searched cells 
   # that are not in path
   for cell in searched:
      if (
         cell not in path and 
         cell is not start and 
         cell is not end and
         cell not in target and
         cell not in finish
      ):
         cell.drawVisit()
         cell.drawGrid()
   
   for cell in target:
      cell.drawTarget()
      cell.drawGrid()
   
   for cell in finish:
      cell.drawFinish()
      cell.drawGrid()
   
   # after trail is draw,
   # teleport focus to start position
   start.drawActive()
   start.drawGrid()

   # wait a short time
   time.sleep(0.07)
   # play target sound
   sound_target.play()
   # then update display
   pygame.display.flip()
   # allow user controls
   isAllowControl = True