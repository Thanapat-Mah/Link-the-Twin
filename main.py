import pygame
import pyautogui
import pprint
from button import Button
from game_panel import GamePanel

### simple locate on screen
# bee = None
# bee = pyautogui.locateOnScreen('assets/bee.png', confidence=.65)
# print(bee)

### screen shot
# screenshot1 = pyautogui.screenshot('tmp/my_screenshot.png')

### functions -------------------------------------------------------------------------

### init object -----------------------------------------------------------------------
game_panel = GamePanel()

set_panel_button = Button(text='Set panel', rect=[10, 10, 80, 30])
set_panel_button.set_is_active(False)
set_panel = True

### run the program -------------------------------------------------------------------
pygame.init()
win = pygame.display.set_mode((300, 100))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # check click button
        if set_panel_button.check_click(event):
            set_panel = set_panel_button.get_is_active()

        # set panel size
        keys = pygame.key.get_pressed()
        if set_panel:
            if keys[pygame.K_t] and (event.type == pygame.KEYDOWN):
                game_panel.panel_topleft = list(pyautogui.position())
                print(f'Top left = {game_panel.panel_topleft}')
                game_panel.calculate_cell_position()
            elif keys[pygame.K_b] and (event.type == pygame.KEYDOWN):
                game_panel.panel_bottomright = list(pyautogui.position())
                print(f'Bottom right = {game_panel.panel_bottomright}')
                game_panel.calculate_cell_position()


    win.fill((10, 10, 10))
    set_panel_button.draw(win)
    pygame.display.update()

pygame.quit()