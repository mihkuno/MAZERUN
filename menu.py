import pygame
import sys
import subprocess

pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 550
SIZE = (WIDTH, HEIGHT)
LIGHT = (239, 239, 239)

ICON = pygame.image.load("./public/icon.png")
SCREEN = pygame.display.set_mode(SIZE)

# create the screens
menuScreen = pygame.Surface(SIZE)
menuScreen.fill(LIGHT)

gameScreen = pygame.Surface(SIZE)
gameScreen.fill(LIGHT)

# set up the display
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Maze Runner")
pygame.display.set_icon(ICON)

# setup the main menu
RED = (255, 107, 107)
GREEN = (46, 204, 113)
BLACK = (0, 0, 0)

bgImg = pygame.image.load("./assets/image/bg_menu.png")
bgImgAspectRatio = bgImg.get_width() / bgImg.get_height()
bgImgH = int(950 / bgImgAspectRatio)
bgImg = pygame.transform.scale(bgImg, (900, bgImgH))
bgImgY = -50  # initial y-position of the background image

titleFont = "./assets/fonts/JoystickBold-62LA.ttf"
titleFont = pygame.font.Font(titleFont, 87)
titleText = titleFont.render("Mazerun", True, BLACK)
titlePosX = WIDTH // 2 - titleText.get_width() // 2
titlePosY = 190
titlePos = (titlePosX, titlePosY)

startFont = "./assets/fonts/TrulyMadlyDpad-a72o.ttf"
startFont = pygame.font.Font(startFont, 27)
startText = startFont.render("Start", True, LIGHT)

# store the original dimensions of the start text
original_text_width, original_text_height = startText.get_width(), startText.get_height()

# initial position and dimensions of the button
startBtnX = WIDTH // 2 - 225 // 2
startBtnY = (HEIGHT // 2 - 53 // 2) + 100
startBtnWidth = 225
startBtnHeight = 53

startBtnRect = pygame.Rect(startBtnX, startBtnY, startBtnWidth, startBtnHeight)

# set initial scale factors
btn_scale = 1.0
zoom_speed = 0.0017  # Adjust the speed of the zooming animation

# set initial values for background image movement
bg_speed = 0.1  # Adjust the speed of the movement
bg_direction = 1  # 1 for down, -1 for up

# initial screen
currentScreen = menuScreen

# create the clock to control the frame rate
clock = pygame.time.Clock()

# load the sounds
sound_click = pygame.mixer.Sound("./assets/audio/click.mp3")
sound_hover = pygame.mixer.Sound("./assets/audio/hover.mp3")
sound_menu = pygame.mixer.Sound("./assets/audio/bg_wires.mp3")
sound_menu.play(-1)

startBtnColor = GREEN
isStartBtnFocused = False
while True:

    if startBtnRect.collidepoint(pygame.mouse.get_pos()):
        btn_scale = 1
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        isStartBtnFocused = True
    else: 
        isStartBtnFocused = False
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif not isStartBtnFocused and startBtnRect.collidepoint(pygame.mouse.get_pos()):
            sound_hover.play()
        
        elif isStartBtnFocused and event.type == pygame.MOUSEBUTTONDOWN:
            startBtnColor = (84, 233, 139)
            sound_click.play()
            subprocess.Popen(["python", "main.py"], shell=True)
            sys.exit()
            
        elif isStartBtnFocused and event.type == pygame.MOUSEBUTTONUP:
            startBtnColor = GREEN


    # idle animation: continuously zoom the button in and out
    if not isStartBtnFocused:
        btn_scale += zoom_speed
        if btn_scale < 1.0 or btn_scale > 1.1:
            zoom_speed = -zoom_speed
            
    # background image movement: move the background image up and down
    bgImgY += bg_speed * bg_direction
    if bgImgY > 1 or bgImgY < -80:
        bg_direction *= -1

    # scale the button rect accordingly
    scaled_btn_rect = startBtnRect
    scaled_btn_rect.width = int(startBtnWidth * btn_scale)
    scaled_btn_rect.height = int(startBtnHeight * btn_scale)

    # adjust the position of the button to keep it centered
    scaled_btn_rect.x = WIDTH // 2 - scaled_btn_rect.width // 2
    scaled_btn_rect.y = (HEIGHT // 2 - scaled_btn_rect.height // 2) + 50

    # maintain the original aspect ratio of the text and scale it within the button rect
    scaled_text_width = int(original_text_width * (scaled_btn_rect.width / startBtnWidth))
    scaled_text_height = int(original_text_height * (scaled_btn_rect.height / startBtnHeight))
    scaled_text = pygame.transform.scale(startText, (scaled_text_width, scaled_text_height))

    # draw the button
    menuScreen.fill(LIGHT)
    pygame.draw.rect(menuScreen, startBtnColor, scaled_btn_rect, 0, 50)
    menuScreen.blit(titleText, titlePos)
    menuScreen.blit(scaled_text, (scaled_btn_rect.x + (scaled_btn_rect.width - scaled_text_width) // 2, scaled_btn_rect.y + (scaled_btn_rect.height - scaled_text_height) // 2))

    # draw the background image with movement
    menuScreen.blit(bgImg, (-150, bgImgY))

    # draw the current screen onto the window
    window.blit(menuScreen, (0, 0))

    # update the display
    pygame.display.flip()

    # cap the frame rate
    clock.tick_busy_loop(60)
