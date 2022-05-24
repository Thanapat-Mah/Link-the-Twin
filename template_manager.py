import pyautogui
# from PIL import Image
import pygame
from datetime import datetime
import os
import shutil

# set current directory
os.chdir(os.getcwd())


folder = f'{os.getcwd()}\\templates'
print(f'Init template folder at: {folder}')


class TemplateManager:
	def __init__(self, cell_count):
		self.__cell_count = cell_count
		self.__templates = dict()

	def get_template_image(self, template_number):
		return pygame.image.load(f'templates/template{template_number}.png')

	def clear_template_folder(self):
		for filename in os.listdir(folder):
		    file_path = os.path.join(folder, filename)
		    try:
		        if os.path.isfile(file_path) or os.path.islink(file_path):
		            os.unlink(file_path)
		        elif os.path.isdir(file_path):
		            shutil.rmtree(file_path)
		    except Exception as e:
		        print('Failed to delete %s. Reason: %s' % (file_path, e))

	def read_template(self, cell_positions, cell_size, distinct=True):
		print('Begin template reading.')
		self.clear_template_folder()
		if not distinct:
			for col in range(self.__cell_count[0]):
				for row in range(self.__cell_count[1]):
					cell_region = (cell_positions[col][row][0], cell_positions[col][row][1], cell_size[0], cell_size[1])
					pyautogui.screenshot(f'templates/template{col:02d}-{row:02d}.png', region=cell_region)
			print(f'{self.__cell_count[0]*self.__cell_count[1]} template is read.')
			return self.__cell_count[0]*self.__cell_count[1]
		else:
			templates = []
			if cell_size[0]*cell_size[1] > 5000:
				match_confidence = 0.7
			else:
				match_confidence = 0.5 + round(cell_size[0]*cell_size[1]*0.2/5000, 2)
			print(f'Set template match confidence to {match_confidence}')
			for col in range(self.__cell_count[0]):
				for row in range(self.__cell_count[1]):
					test_scale_x = int(cell_size[0]/3)
					test_scale_y = int(cell_size[1]/3)
					test_cell_region = (cell_positions[col][row][0]+test_scale_x, cell_positions[col][row][1]+test_scale_y,
						test_scale_x, test_scale_y)
					test_template = pyautogui.screenshot('templates/test_template.png', region=test_cell_region)
					template_exist = False
					for exist_template in templates:
						if pyautogui.locate(test_template, exist_template, confidence=match_confidence):
							template_exist = True
					if not template_exist:
						scale_x = cell_size[0]/100
						scale_y = cell_size[1]/100
						cell_region = (cell_positions[col][row][0]+int((col+10)*scale_x),
							cell_positions[col][row][1]+int((row+10)*scale_y),
							int(85*scale_x),
							int(85*scale_y))
						# cell_region = (cell_positions[col][row][0],
						# 	cell_positions[col][row][1],
						# 	cell_size[0],
						# 	cell_size[1])
						template = pyautogui.screenshot('templates/current_template.png', region=cell_region)
						templates.append(template)
			i = 1
			for template in templates:
				template.save(f'templates/template{i}.png')
				self.__templates[str(i)] = template
				i += 1
			os.remove('templates/test_template.png')
			os.remove('templates/current_template.png')
			print(f'{i-1} template is read.')
			return len(templates), match_confidence

	def locate_match_templates(self, template_number, region, panel_topleft, confidence=0.7):
		# match_list = []
		# for im in pyautogui.locateAllOnScreen(f'templates/template{template_number}.png',
		# 	confidence=.5, region=region, grayscale=True):
		# 	location = (im.left, im.top)
		# 	match_list.append(location)
		# return match_list
		match_list = []
		game_panel = pyautogui.screenshot(region=region)
		template = self.__templates[str(template_number)]
		for im in pyautogui.locateAll(template, game_panel, confidence=confidence, grayscale=True):
			location = (im.left + panel_topleft[0], im.top + panel_topleft[1])
			match_list.append(location)
		return match_list