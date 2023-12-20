import pygame
import sys
import subprocess
from setting import run_settings

# Initialize Pygame
pygame.init()


# Constants
WIDTH, HEIGHT = 600, 600
FPS = 60

# Colors
DEEP_SPACE_SPARKLE = (66, 101, 112)
OLD_BURGUNDY = (76, 50, 50)
GIANTS_CLUB = (184, 94, 79)
PERSIAN_ORANGE = (214, 154, 83)
BONE = (225, 213, 200)
DARK_SEA_GREEN = (146, 178, 135)

# Create the main menu screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MAZERUN")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font("fonts\Arcade.ttf", 150)
button_font = pygame.font.Font(None, 36)

# Buttons
play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
settings_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)

while True:
    screen.fill(DEEP_SPACE_SPARKLE)

    # Draw buttons
    pygame.draw.rect(screen, OLD_BURGUNDY, play_button)
    pygame.draw.rect(screen, GIANTS_CLUB, settings_button)
    pygame.draw.rect(screen, OLD_BURGUNDY, exit_button)

    # Draw text
    title_text = title_font.render("MAZERUN", True, BONE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    play_text = button_font.render("Play", True, BONE)
    screen.blit(play_text, (play_button.x + 72, play_button.y + 15))

    settings_text = button_font.render("Settings", True, BONE)
    screen.blit(settings_text, (settings_button.x + 52, settings_button.y + 15))

    exit_text = button_font.render("Exit", True, BONE)
    screen.blit(exit_text, (exit_button.x + 72, exit_button.y + 15))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(pygame.mouse.get_pos()):
                print("Play button clicked!")
                pygame.quit()
                subprocess.run(["python", "main.py"])  # Replace "main.py" with your actual file
            elif settings_button.collidepoint(pygame.mouse.get_pos()):
                print("Settings button clicked!")
                run_settings()
            elif exit_button.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()

    pygame.display.flip()
    clock.tick(FPS)