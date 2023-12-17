import sys
sys.path.append('./lib')

import pygame
import maze

if __name__ == "__main__":
   
   pygame.init()

   width = 600
   height = 600
   
   size = (width, height) 
   screen = pygame.display.set_mode(size)
   icon_image = pygame.image.load("./public/icon.png")
   
   pygame.display.set_caption("Maze Runner")
   pygame.display.set_icon(icon_image)
   
   maze.width = 600
   maze.height = 600
   maze.screen = screen
   maze.create()
   maze.render()