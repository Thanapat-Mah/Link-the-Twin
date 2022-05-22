class GamePanel:
    def __init__(self):
        self.panel_topleft = [0, 0]     # [x, y]
        self.panel_bottomright = [1920, 1080]
        self.cell_count = [14, 7]
        self.cell_size = [0, 0]
        self.cell_position = [[[0, 0] for row in range(self.cell_count[1])] for col in range(self.cell_count[0])]
        self.calculate_cell_position()
        print(f'Init game panel with {self.cell_count[0]}x{self.cell_count[1]} cells.')

    def calculate_cell_position(self, estimate=True):
        delta_x = int((self.panel_bottomright[0] - self.panel_topleft[0])/self.cell_count[0])
        delta_y = int((self.panel_bottomright[1] - self.panel_topleft[1])/self.cell_count[1])
        self.cell_size[0] = delta_x
        self.cell_size[1] = delta_y
        if estimate:
            self.cell_size[0] -= 40
            self.cell_size[1] -= 40
        # print(f'Delta x = {delta_x}, Delta y = {delta_y}')
        cell_x = self.panel_topleft[0]
        if estimate: cell_x += 20
        for col in range(self.cell_count[0]):
            cell_y = self.panel_topleft[0]
            if estimate: cell_y += 20
            for row in range(self.cell_count[1]):
                self.cell_position[col][row] = [cell_x, cell_y]
                cell_y += delta_y
            cell_x += delta_x
            # print(self.cell_position[col])