import sys
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
   
   # set maze grid
   maze.screen = screen
   maze.area = 400
   maze.w = 100
   
   # center the maze
   maze.xOffset = (width - maze.w * (maze.area // maze.w)) // 2
   maze.yOffset = (height - maze.w * (maze.area // maze.w)) // 2 - 20

   # load sounds
   maze.sound_target = pygame.mixer.Sound("./assets/audio/join.ogg")
   maze.sound_move = pygame.mixer.Sound("./assets/audio/tap.wav") 
   maze.sound_wall = pygame.mixer.Sound("./assets/audio/wall.wav")
   
   maze.create()
   maze.render()