import pyautogui
from datetime import datetime
import os

# set current directory
os.chdir(os.getcwd())

class TemplateManager:
	def __init__(self, cell_count):
		self.__cell_count = cell_count

	# def read_template(self, cell_positions, cell_size, distinct=False):
	# 	# timestamp = datetime.now().strftime('%d/%m/%Y_%H:%M:%S')
	# 	for col in range(self.__cell_count[0]):
	# 		for row in range(self.__cell_count[1]):
	# 			cell_region = (cell_positions[col][row][0], cell_positions[col][row][1], cell_size[0], cell_size[1])
	# 			pyautogui.screenshot(f'tmp/template{col:02d}-{row:02d}.png', region=cell_region)

	def read_template(self, cell_positions, cell_size, distinct=True):
		if not distinct:
			for col in range(self.__cell_count[0]):
				for row in range(self.__cell_count[1]):
					cell_region = (cell_positions[col][row][0], cell_positions[col][row][1], cell_size[0], cell_size[1])
					pyautogui.screenshot(f'tmp/template{col:02d}-{row:02d}.png', region=cell_region)
		else:
			templates = []
			for col in range(self.__cell_count[0]):
				for row in range(self.__cell_count[1]):
					cell_region = (cell_positions[col][row][0], cell_positions[col][row][1], cell_size[0], cell_size[1])
					test_scale_x = int(cell_size[0]/4)
					test_scale_y = int(cell_size[1]/4)
					test_cell_region = (cell_positions[col][row][0]+test_scale_x, cell_positions[col][row][1]+test_scale_y, 2*test_scale_x, 2*test_scale_y)
					test_template = pyautogui.screenshot('tmp/test_template.png', region=test_cell_region)
					template_exist = False
					for exist_template in templates:
						if pyautogui.locate(test_template, exist_template, confidence=.65):
							template_exist = True
					if not template_exist:
						template = pyautogui.screenshot('tmp/current_template.png', region=cell_region)
						templates.append(template)
			i = 1
			for template in templates:
				template.save(f'tmp/template{i}.png')
				i += 1
			os.remove('tmp/test_template.png')
			os.remove('tmp/current_template.png')



	def locate_match_template(self, template_number):
		for im in pyautogui.locateAllOnScreen(f'tmp/template{template_number}.png', confidence=.9):
			print(im)