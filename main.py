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
   screen = pygame.display.set_mode(size)
   icon_image = pygame.image.load("./public/icon.png")
   
   pygame.display.set_caption("Maze Runner")
   pygame.display.set_icon(icon_image)
   
   maze.sound_target = pygame.mixer.Sound("./assets/audio/target.ogg")
   maze.sound_move = pygame.mixer.Sound("./assets/audio/tap.wav") 
   maze.sound_wall = pygame.mixer.Sound("./assets/audio/wall.wav")
   maze.width = 600
   maze.height = 600
   maze.screen = screen
   maze.create()
   maze.render()