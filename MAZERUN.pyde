import Maze

# current view status
status = 'generate'

# prevent hold pressed
up_key_pressed = False
down_key_pressed = False
left_key_pressed = False
right_key_pressed = False
      
    
def setup():
    size(600, 600)
    
    # animate initial maze generation
    frameRate(20)
    
    # create the grid
    Maze.create()
       

def draw():    
    global status
    background(200)
    
    Maze.render()

    if status == 'generate':
        # generate wall paths on grid
        Maze.generate()
        
        if Maze.isGenerated is True:
            status = 'game'
            frameRate(60)
            
            print('Maze generation complete')
            

def keyPressed():
    global status
    global up_key_pressed
    global down_key_pressed
    global left_key_pressed
    global right_key_pressed

    if status == 'game':
        if keyCode == UP and not up_key_pressed:
            up_key_pressed = True
            Maze.moveTop()
        
        elif keyCode == DOWN and not down_key_pressed:
            down_key_pressed = True
            Maze.moveBottom()
        
        elif keyCode == LEFT and not left_key_pressed:
            left_key_pressed = True
            Maze.moveLeft()
            
        elif keyCode == RIGHT and not right_key_pressed:
            right_key_pressed = True
            Maze.moveRight()
    

def keyReleased():
    global status
    global up_key_pressed
    global down_key_pressed
    global left_key_pressed
    global right_key_pressed

    if status == 'game':
        if keyCode == UP:
            up_key_pressed = False
        
        elif keyCode == DOWN:
            down_key_pressed = False
        
        elif keyCode == LEFT:
            left_key_pressed = False
        
        elif keyCode == RIGHT:
            right_key_pressed = False
