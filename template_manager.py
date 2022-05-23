import pyautogui
from datetime import datetime
import os

# set current directory
os.chdir(os.getcwd())

class TemplateManager:
	def __init__(self, cell_count):
		self.__cell_count = cell_count

	def read_template(self, cell_positions, cell_size, distinct=True):
		if not distinct:
			for col in range(self.__cell_count[0]):
				for row in range(self.__cell_count[1]):
					cell_region = (cell_positions[col][row][0], cell_positions[col][row][1], cell_size[0], cell_size[1])
					pyautogui.screenshot(f'templates/template{col:02d}-{row:02d}.png', region=cell_region)
			return self.__cell_count[0]*self.__cell_count[1]
		else:
			templates = []
			for col in range(self.__cell_count[0]):
				for row in range(self.__cell_count[1]):
					test_scale_x = int(cell_size[0]/5)
					test_scale_y = int(cell_size[1]/5)
					test_cell_region = (cell_positions[col][row][0]+test_scale_x, cell_positions[col][row][1]+test_scale_y,
						3*test_scale_x, 3*test_scale_y)
					test_template = pyautogui.screenshot('templates/test_template.png', region=test_cell_region)
					template_exist = False
					for exist_template in templates:
						if pyautogui.locate(test_template, exist_template, confidence=.5):
							template_exist = True
					if not template_exist:
						scale_x = int(cell_size[0]/10)
						scale_y = int(cell_size[1]/10)
						cell_region = (cell_positions[col][row][0]+scale_x, cell_positions[col][row][1]+scale_y,
							9*scale_x, 9*scale_y)
						template = pyautogui.screenshot('templates/current_template.png', region=cell_region)
						templates.append(template)
			i = 1
			for template in templates:
				template.save(f'templates/template{i}.png')
				i += 1
			os.remove('templates/test_template.png')
			os.remove('templates/current_template.png')
			return len(templates)

	def locate_match_templates(self, template_number, region):
		match_list = []
		for im in pyautogui.locateAllOnScreen(f'templates/template{template_number}.png', confidence=.5, region=region):
			location = (im.left, im.top)
			match_list.append(location)
		return match_list