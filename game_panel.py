import pygame
from path_finder import PathFinder

pygame.font.init()
font_consola = pygame.font.Font('./CONSOLA.TTF', 12)

class GamePanel:
    def __init__(self):
        self.__panel_topleft = [0, 0]     # [x, y]
        self.__panel_bottomright = [1920, 1080]
        self.__cell_count = [14, 8]
        self.__cell_size = [0, 0]
        self.__cell_labels = [[False for row in range(self.__cell_count[1])] for col in range(self.__cell_count[0])]
        self.__cell_positions = [[[0, 0] for row in range(self.__cell_count[1])] for col in range(self.__cell_count[0])]
        self.calculate_cell_position()
        self.__padded_cells = self.__cell_labels.copy()
        self.padding_cells()
        self.__templates_count = 0
        self.__match_data = []
        self.__initial_match_confidence = 0.7
        self.__match_confidence = 0.7
        print(f'Init game panel with {self.__cell_count[0]}x{self.__cell_count[1]} cells.')

    def get_cell_count(self):
        return self.__cell_count

    def get_cell_positions(self):
        return self.__cell_positions

    def get_cell_size(self):
        return self.__cell_size

    def get_topleft(self):
        print(f'Set panel topleft to {self.__panel_topleft}')
        return self.__panel_topleft

    def get_bottomright(self):
        print(f'Set panel bottomright to {self.__panel_bottomright}')
        return self.__panel_bottomright

    def get_panel_region(self):
        region = []
        region.append(self.__panel_topleft[0])
        region.append(self.__panel_topleft[1])
        region.append(self.__panel_bottomright[0] - self.__panel_topleft[0])
        region.append(self.__panel_bottomright[1] - self.__panel_topleft[1])
        return region

    def get_cell_labels(self):
        return self.__cell_labels

    def get_padded_cells(self):
        return self.__padded_cells

    def set_topleft(self, new_topleft):
        self.__panel_topleft = new_topleft

    def set_bottomright(self, new_bottomright):
        self.__panel_bottomright = new_bottomright

    def set_templates_count(self, new_templates_count):
        self.__templates_count = new_templates_count

    def set_initial_match_confidence(self, confidence):
        self.__initial_match_confidence = confidence
        self.__match_confidence = self.__initial_match_confidence

    def reset_cell_labels(self):
        for col in range(len(self.__cell_labels)):
            for row in range(len(self.__cell_labels[col])):
                self.__cell_labels[col][row] = 0

    # calculate position for screeenshot the cells
    def calculate_cell_position(self):
        delta_x = int((self.__panel_bottomright[0] - self.__panel_topleft[0])/self.__cell_count[0])
        delta_y = int((self.__panel_bottomright[1] - self.__panel_topleft[1])/self.__cell_count[1])
        self.__cell_size[0] = delta_x
        self.__cell_size[1] = delta_y
        # print(f'Delta x = {delta_x}, Delta y = {delta_y}')
        cell_x = self.__panel_topleft[0]
        for col in range(self.__cell_count[0]):
            cell_y = self.__panel_topleft[1]
            for row in range(self.__cell_count[1]):
                self.__cell_positions[col][row] = [cell_x, cell_y]
                cell_y += delta_y
            cell_x += delta_x
            # print(self.__cell_positions[col])

    # label cells according to templates found
    def label_cells(self, template_manager):
        self.reset_cell_labels()
        for template_index in range(1, self.__templates_count+1):
            match_templates_location = template_manager.locate_match_templates(
                template_index,
                self.get_panel_region(),
                self.__panel_topleft,
                self.__match_confidence)
            for location in match_templates_location:
                cell_col = int((location[0] - self.__panel_topleft[0])/self.__cell_size[0])
                cell_row = int((location[1] - self.__panel_topleft[1])/self.__cell_size[1])
                if (cell_col >= 0) and (cell_col < self.__cell_count[0]):
                    if (cell_row >= 0) and (cell_row < self.__cell_count[1]):
                        self.__cell_labels[cell_col][cell_row] = template_index
        # print(self.__cell_labels)
    
    # add zero-padding for the cell_labels
    def padding_cells(self):
        padded_cells = []
        # add left padding
        padded_cells.append([0 for i in range(self.__cell_count[1]+2)])
        for col in range(self.__cell_count[0]):
            padded_col = self.__cell_labels[col].copy()
            padded_col.insert(0, 0)     # add top padding of column
            padded_col.insert(len(padded_col), 0)    # add bottom padding of column
            padded_cells.append(padded_col)
        # add right padding
        padded_cells.append([0 for i in range(self.__cell_count[1]+2)])
        # print(padded_cells)
        self.__padded_cells = padded_cells
        return padded_cells

    # find the path between same template on cells
    def match_template(self):
        self.__match_data = PathFinder.match_template(self.__padded_cells)
        if self.__match_data == None:
            if self.__match_confidence > 0.1:
                self.__match_confidence *= 0.9
                print(f'Decrease confidence to {self.__match_confidence}')
            else:
                print(f'Lowest confidence = {self.__match_confidence}')
        else:
            if self.__match_confidence < self.__initial_match_confidence:
                self.__match_confidence = self.__initial_match_confidence
                print(f'Reset confidence to {self.__initial_match_confidence}')

    # draw the padded cell labels
    def draw(self, display, template_manager):
        draw_cell_size = 20
        cell_x = 65     # (450 - 16*20)/2
        cell_y = 110    # (450 - 100 - 9*20)/2 + 50
        for col in range(len(self.__padded_cells)):
            for row in range(len(self.__padded_cells[0])):
                cell = self.__padded_cells[col][row]
                # if its nothing, color with black
                if cell == 0:
                    color = (50, 50, 50)
                # if it has label, color with white
                else:
                    color = (255, 255, 255)
                rect = (cell_x, cell_y, draw_cell_size, draw_cell_size)
                pygame.draw.rect(display, color, rect)
                cell_y += draw_cell_size
            cell_x += draw_cell_size
            cell_y = 110

        # highlight matched cell
        match_template = None
        match_cells = []
        match_path = []
        # highlight matched templates with red
        if self.__match_data:
            match_template = self.__match_data[0]
            match_cells = self.__match_data[1:3]
            for match_cell in match_cells:
                cell_x = 65 + match_cell[0]*draw_cell_size
                cell_y = 110 + match_cell[1]*draw_cell_size
                rect = (cell_x, cell_y, draw_cell_size, draw_cell_size)
                pygame.draw.rect(display, (255, 120, 120), rect)
            # highlight path with yellow
            if len(self.__match_data) > 3:
                match_path = self.__match_data[3]
                for path_cell in match_path:
                    cell_x = 65 + path_cell[0]*draw_cell_size + int(draw_cell_size/4)
                    cell_y = 110 + path_cell[1]*draw_cell_size + int(draw_cell_size/4)
                    rect = (cell_x, cell_y,
                        draw_cell_size - int(draw_cell_size/2),
                        draw_cell_size - int(draw_cell_size/2))
                    pygame.draw.rect(display, (255, 255, 120), rect)

        # show the matched template
        template_x = 175    # (450 - 100)/2
        template_y = 320    # (110 + 9*20) + middle padding
        rect = (template_x, template_y, 100, 100)
        if match_template:
            template_image = template_manager.get_template_image(match_template)
            template_image = pygame.transform.scale(template_image, (100, 100))
            display.blit(template_image, (template_x, template_y))
        else:
            pygame.draw.rect(display, (50, 50, 50), rect)
            text_surface = font_consola.render('No Matched.', True, (255, 255, 255))
            display.blit(text_surface, (template_x+10, template_y+40))