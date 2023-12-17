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
   
   maze.sound_target = pygame.mixer.Sound("./assets/audio/target.ogg")
   maze.sound_move = pygame.mixer.Sound("./assets/audio/tap.wav") 
   maze.sound_wall = pygame.mixer.Sound("./assets/audio/wall.wav")
   maze.screen = screen
   maze.xOffset = 50
   maze.yOffset = 50
   maze.area = 500
   maze.w = 20
   maze.create()
   maze.render()