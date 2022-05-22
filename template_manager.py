import pyautogui
from datetime import datetime

class TemplateManager:
	def __init__(self, cell_count):
		self.__cell_count = cell_count

	def read_template(self, cell_positions, cell_size, distinct=False):
		timestamp = datetime.now().strftime('%d/%m/%Y_%H:%M:%S')
		for col in range(self.__cell_count[0]):
			for row in range(self.__cell_count[1]):
				cell_region = (cell_positions[col][row][0], cell_positions[col][row][1], cell_size[0], cell_size[1])
				pyautogui.screenshot(f'tmp/template{col:02d}-{row:02d}.png', region=cell_region)

	def locate_match_template(self, template_number):
		print(pyautogui.locateOnScreen(f'tmp/template{template_number}.png', confidence=.65))