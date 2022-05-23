import pygame

class GamePanel:
    def __init__(self):
        self.__panel_topleft = [0, 0]     # [x, y]
        self.__panel_bottomright = [1920, 1080]
        self.__cell_count = [14, 7]
        self.__cell_size = [0, 0]
        self.__cell_labels = [[False for row in range(self.__cell_count[1])] for col in range(self.__cell_count[0])]
        self.__cell_positions = [[[0, 0] for row in range(self.__cell_count[1])] for col in range(self.__cell_count[0])]
        self.calculate_cell_position()
        self.__padded_cells = self.__cell_labels.copy()
        self.padding_cells()
        self.__templates_count = 0
        print(f'Init game panel with {self.__cell_count[0]}x{self.__cell_count[1]} cells.')

    def get_cell_count(self):
        return self.__cell_count

    def get_cell_positions(self):
        return self.__cell_positions

    def get_cell_size(self):
        return self.__cell_size

    def get_topleft(self):
        return self.__panel_topleft

    def get_bottomright(self):
        return self.__panel_bottomright

    def get_panel_region(self):
        region = []
        region.append(self.__panel_topleft[0])
        region.append(self.__panel_topleft[1])
        region.append(self.__panel_bottomright[0] - self.__panel_topleft[0])
        region.append(self.__panel_bottomright[1] - self.__panel_topleft[1])
        return region

    def set_topleft(self, new_topleft):
        self.__panel_topleft = new_topleft

    def set_bottomright(self, new_bottomright):
        self.__panel_bottomright = new_bottomright

    def set_templates_count(self, new_templates_count):
        self.__templates_count = new_templates_count

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
        for template_index in range(1, self.__templates_count+1):
            match_templates_location = template_manager.locate_match_templates(str(template_index), self.get_panel_region())
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

    # draw the padded cell labels
    def draw(self, display):
        draw_cell_size = 20
        cell_x = 65    # (450 - 16*20)/2
        cell_y = 110    # (300 - 9*20)/2 + 50
        for col in self.__padded_cells:
            for cell in col:
                if cell == 0:
                    color = (50, 50, 50)
                else:
                    color = (255, 255, 255)
                rect = (cell_x, cell_y, draw_cell_size, draw_cell_size)
                pygame.draw.rect(display, color, rect)
                cell_y += draw_cell_size
            cell_x += draw_cell_size
            cell_y = 110
        