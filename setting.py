# settings.py

import pygame
import os

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

# Create the settings menu screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settings Menu")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font("fonts\Arcade.ttf", 150)
button_font = pygame.font.Font(None, 36)

# Buttons
music_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 10, 200, 50)
back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)

def run_settings():
    global screen  # Reference the global screen variable

    # Main settings loop
    settings_running = True
    while settings_running:
        screen.fill(DEEP_SPACE_SPARKLE)

        # Draw buttons
        pygame.draw.rect(screen, OLD_BURGUNDY, back_button)
        pygame.draw.rect(screen, OLD_BURGUNDY, music_button)

        # Draw text
        title_text = title_font.render("SETTINGS", True, BONE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        music_text = button_font.render("Music ON", True, BONE)
        screen.blit(music_text, (music_button.x + 48, music_button.y + 15))

        back_text = button_font.render("Back", True, BONE)
        screen.blit(back_text, (back_button.x + 65, back_button.y + 15))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(pygame.mouse.get_pos()):
                    settings_running = False
                    return True

                elif music_button.collidepoint(pygame.mouse.get_pos()):
                    # Toggle the music state or handle music-related operations
                    print("Music button clicked! Toggle the music state.")

        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
