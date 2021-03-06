import pygame
import pyautogui
import pprint
import time
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
    active_color=(100, 200, 100))

match_template_button = Button(text='Match template', rect=[310, 10, 130, 30],
    active_color=(100, 200, 100))
match_template_button.set_is_active(False)

### run the program -------------------------------------------------------------------
pygame.init()
font_consola = pygame.font.Font('./CONSOLA.TTF', 12)
win = pygame.display.set_mode((450, 450))
topleft_text = '[0, 0]'
bottomright_text = '[1920, 1080]'
auto_match = False
count = 0
run = True
while run:
    for event in pygame.event.get():
        this_round_match = False
        if event.type == pygame.QUIT:
            run = False

        ### check for button clicking
        # enable set panel corner mode
        if set_panel_button.check_click(event):
            set_panel = set_panel_button.get_is_active()
        # read templates in panel
        elif read_template_button.check_click(event):
            read_template_button.draw(win)
            pygame.display.update()
            template_manager.set_region(game_panel.get_panel_region())
            template_manager.set_old_screen()
            templates_count, match_confidence = template_manager.read_template(game_panel.get_cell_positions(), game_panel.get_cell_size())
            game_panel.set_templates_count(templates_count)
            game_panel.set_initial_match_confidence(match_confidence)
            read_template_button.set_is_active(True)
        # match_template templates in panel
        elif match_template_button.check_click(event):
            auto_match = match_template_button.get_is_active()
            if auto_match:
                match_template_button.draw(win)
            game_panel.label_cells(template_manager)
            game_panel.padding_cells()
            game_panel.match_template()

            game_panel.draw(win, template_manager)
            # match_template_button.draw(win)
            pygame.display.update()

        # set panel size
        keys = pygame.key.get_pressed()
        if set_panel:
            # press 't' to set topleft point
            if keys[pygame.K_t] and (event.type == pygame.KEYDOWN):
                game_panel.set_topleft(list(pyautogui.position()))
                game_panel.calculate_cell_position()
                topleft_text = str(game_panel.get_topleft())
            # press 'b' to set bottomright point
            elif keys[pygame.K_b] and (event.type == pygame.KEYDOWN):
                game_panel.set_bottomright(list(pyautogui.position()))
                game_panel.calculate_cell_position()
                bottomright_text = str(game_panel.get_bottomright())

    if auto_match:
        start_time = time.time()

        if template_manager.is_screen_change():
            game_panel.label_cells(template_manager)
            game_panel.padding_cells()
            game_panel.match_template()

            game_panel.draw(win, template_manager)
            # match_template_button.draw(win)
            pygame.display.update()

            print(f'> Elasped = {time.time()-start_time:.3f} sec')
    else:
        # refresh window
        win.fill((10, 10, 10))
        # draw components
        set_panel_button.draw(win)
        read_template_button.draw(win)
        match_template_button.draw(win)
        game_panel.draw(win, template_manager)

        # draw panel position
        topleft_text_surface = font_consola.render(topleft_text, True, (255, 255, 255))
        win.blit(topleft_text_surface, (10, 55))
        bottomright_text_surface = font_consola.render(bottomright_text, True, (255, 255, 255))
        win.blit(bottomright_text_surface, (10, 75))

    pygame.display.update()

pygame.quit()