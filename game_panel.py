class GamePanel:
    def __init__(self):
        self.__panel_topleft = [0, 0]     # [x, y]
        self.__panel_bottomright = [1920, 1080]
        self.__cell_count = [14, 7]
        self.__cell_size = [0, 0]
        self.__cell_positions = [[[0, 0] for row in range(self.__cell_count[1])] for col in range(self.__cell_count[0])]
        self.calculate_cell_position()
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

    def set_topleft(self, new_topleft):
        self.__panel_topleft = new_topleft

    def set_bottomright(self, new_bottomright):
        self.__panel_bottomright = new_bottomright

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