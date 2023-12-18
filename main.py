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
   maze.area = 500
   maze.w = 50
   
   # center the maze
   maze.xOffset = (width - maze.w * (maze.area // maze.w)) // 2
   maze.yOffset = (height - maze.w * (maze.area // maze.w)) // 2

   # load sounds
   maze.sound_target = pygame.mixer.Sound("./assets/audio/begin.ogg")
   maze.sound_move = pygame.mixer.Sound("./assets/audio/tap.wav") 
   maze.sound_wall = pygame.mixer.Sound("./assets/audio/wall.wav")
   maze.sound_clear = pygame.mixer.Sound("./assets/audio/hover.mp3")
   maze.sound_trail = pygame.mixer.Sound("./assets/audio/go.wav")
   
   maze.create()
   maze.render()