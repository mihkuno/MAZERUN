import sys
import subprocess
sys.path.append('./lib')

import pygame
import maze

if __name__ == "__main__":
   
   pygame.init()
   pygame.mixer.init()
   
   width = 600
   height = 600
   size = (width, height) 
   background = (239, 239, 239)
   
   icon = pygame.image.load("./public/icon.png")
   screen = pygame.display.set_mode(size)
   
   pygame.display.set_caption("Maze Runner")
   pygame.display.set_icon(icon)
   screen.fill(background)
   
   # load sounds
   maze.sound_level = pygame.mixer.Sound("./assets/audio/begin.ogg")
   maze.sound_found = pygame.mixer.Sound("./assets/audio/notify.wav")
   maze.sound_target = pygame.mixer.Sound("./assets/audio/join.ogg")
   maze.sound_move = pygame.mixer.Sound("./assets/audio/tap.wav") 
   maze.sound_wall = pygame.mixer.Sound("./assets/audio/wall.wav")
   maze.sound_clear = pygame.mixer.Sound("./assets/audio/hover.mp3")
   maze.sound_trail = pygame.mixer.Sound("./assets/audio/go.wav")
   
   # set maze grid
   maze.screen = screen
   maze.area = 500
   
   # start at level 1
   maze.level = 1
   
   while True:
      # level properties
      if maze.level == 1:
         maze.w = 90
         maze.targetLimit = 1
         
      elif maze.level == 2:
         maze.w = 80
         maze.targetLimit = 2

      elif maze.level == 3:
         maze.w = 60
         maze.targetLimit = 3

      elif maze.level == 4:
         maze.w = 40
         maze.targetLimit = 5
         
      elif maze.level == 5:
         maze.w = 20
         maze.targetLimit = 7
         
      elif maze.level == 6: 
         subprocess.Popen(["python", "end.py"])
         break
      
      elif maze.level == -1:
         print('Game Over!')
         break
      
      # center the maze
      maze.xOffset = (width - maze.w * (maze.area // maze.w)) // 2
      maze.yOffset = (height - maze.w * (maze.area // maze.w)) // 2
      
      maze.create() # game setup
      maze.render() # game loop