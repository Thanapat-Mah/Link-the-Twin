import pygame
import pyautogui
import pprint
from button import Button
from game_panel import GamePanel
from template_manager import TemplateManager

### simple locate on screen
# bee = None
# bee = pyautogui.locateOnScreen('assets/bee.png', confidence=.65)
# print(bee)

### functions -------------------------------------------------------------------------

### init object -----------------------------------------------------------------------
game_panel = GamePanel()
template_manager = TemplateManager(game_panel.get_cell_count())

set_panel_button = Button(text='Set panel', rect=[10, 10, 130, 30])
set_panel_button.set_is_active(False)
set_panel = True

read_template_button = Button(text='Read template', rect=[160, 10, 130, 30],
    active_color=(100, 200, 100), passive_color=(100, 200, 100))

locate_button = Button(text='Locate', rect=[310, 10, 130, 30],
    active_color=(100, 200, 100), passive_color=(100, 200, 100))

### run the program -------------------------------------------------------------------
pygame.init()
font_consola = pygame.font.Font('./CONSOLA.TTF', 12)
win = pygame.display.set_mode((450, 100))
topleft_text = '[0, 0]'
bottomright_text = '[1920, 1080]'
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # check click button
        if set_panel_button.check_click(event):
            set_panel = set_panel_button.get_is_active()
        elif read_template_button.check_click(event):
            template_manager.read_template(game_panel.get_cell_positions(), game_panel.get_cell_size())
        elif locate_button.check_click(event):
            template_manager.locate_match_template('05-05')

        # set panel size
        keys = pygame.key.get_pressed()
        if set_panel:
            if keys[pygame.K_t] and (event.type == pygame.KEYDOWN):
                game_panel.set_topleft(list(pyautogui.position()))
                game_panel.calculate_cell_position()
                topleft_text = str(game_panel.get_topleft())
            elif keys[pygame.K_b] and (event.type == pygame.KEYDOWN):
                game_panel.set_bottomright(list(pyautogui.position()))
                game_panel.calculate_cell_position()
                bottomright_text = str(game_panel.get_bottomright())

    # refresh window
    win.fill((10, 10, 10))
    set_panel_button.draw(win)
    read_template_button.draw(win)
    locate_button.draw(win)

    # draw panel position
    topleft_text_surface = font_consola.render(topleft_text, True, (255, 255, 255))
    win.blit(topleft_text_surface, (10, 55))
    bottomright_text_surface = font_consola.render(bottomright_text, True, (255, 255, 255))
    win.blit(bottomright_text_surface, (10, 75))

    pygame.display.update()

pygame.quit()