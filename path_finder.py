import pygame
import copy

class Path:
	def __init__(self, origin, cell):
		self.__origin = origin
		self.__path = [origin, cell]
		self.__line_count = 1

	def __str__(self):
		return f'{self.__path}'

	def get_origin(self):
		return self.__origin

	def get_terminal(self):
		return self.__path[-1]

	def get_middle_path(self):
		return self.__path[1:-1]

	def grow(self, new_cell):
		if self.is_direction_change(new_cell):
			self.__line_count += 1
		self.__path.append(new_cell)

	def is_direction_change(self, new_cell):
		cell1 = self.__path[-2]
		cell2 = self.__path[-1]
		cell3 = new_cell
		# calculate old direction
		old_direction = (cell2[0] - cell1[0], cell2[1] - cell1[1])
		new_direction = (cell3[0] - cell2[0], cell3[1] - cell2[1])
		if old_direction != new_direction:
			return True
		return False

	def verify(self, new_cell):
		line_count = self.__line_count
		if self.is_direction_change(new_cell):
			line_count += 1
		if (line_count <= 3) and (new_cell not in self.__path):
			return True
		else:
			return False

class PathFinder:
	@classmethod
	def match_template(cls, padded_cells):
		match_data = None
		match_data = cls.find_adjacent(padded_cells)
		if match_data:
			return match_data
		match_data = cls.find_path(padded_cells)
		return match_data

	# find cells with same label in four adjacent connectivity
	@classmethod
	def find_adjacent(cls, padded_cells):
		match_data = None
		original_padded_cells = padded_cells.copy()
		limit_x = len(padded_cells) - 2
		limit_y = len(padded_cells[0]) - 2
		for current_x in range(1, limit_x + 1):
			for current_y in range(1, limit_y + 1):
				neighbors_position = []
				neighbors_position.append((current_x + 1, current_y))
				neighbors_position.append((current_x, current_y + 1))
				current_label = original_padded_cells[current_x][current_y]
				if current_label != 0:
					for neighbor_position in neighbors_position:
						neighbor_label = original_padded_cells[neighbor_position[0]][neighbor_position[1]]
						if neighbor_label == current_label:
							# print(f'Found adjacent at ({current_x}, {current_y})')
							# print(f'      adjacent with ({neighbor_position[0]}, {neighbor_position[1]})')
							# print(f'      template number is {current_label}')
							match_data = [current_label] 	# [label, (current position), (neighbor position)]
							match_data.append((current_x, current_y))
							match_data.append((neighbor_position[0], neighbor_position[1]))
							return match_data
		return match_data

	@classmethod
	def find_path(cls, padded_cells):
		match_data = None
		explored_template = []
		original_padded_cells = padded_cells.copy()
		limit_x = len(padded_cells) - 2
		limit_y = len(padded_cells[0]) - 2
		found_match = False
		for current_x in range(1, limit_x + 1):
			if found_match:
				break
			for current_y in range(1, limit_y + 1):
				if found_match:
					break
				current_label = original_padded_cells[current_x][current_y]
				if current_label == 0:
					continue
				current_cell = (current_x, current_y)
				# find path only if it connect with blank cell (label = 0)
				possible_grow_cells = cls.find_growable_cells(padded_cells, (current_x, current_y), current_label)
				if not possible_grow_cells:
					continue
				# find path only if it not in explored template number
				if current_label in explored_template:
					continue
				explored_template.append(current_label)
				# find the path
				# initiate all path
				paths = []
				for possible_grow_cell in possible_grow_cells:
					paths.append(Path(current_cell, possible_grow_cell))
				# grow path until match or there are no growable path left
				found_path = None
				while (len(paths) > 0) and (not found_match):
					new_paths = []
					# grow every path
					for path in paths:
						possible_grow_cells = cls.find_growable_cells(padded_cells, path.get_terminal(), current_label)
						if not possible_grow_cells:
							continue
						if found_match:
							break
						# add valid new growth path
						for possible_grow_cell in possible_grow_cells:
							if path.verify(possible_grow_cell):
								new_path = copy.deepcopy(path)
								new_path.grow(possible_grow_cell)
								new_paths.append(new_path)
								if current_label == padded_cells[new_path.get_terminal()[0]][new_path.get_terminal()[1]]:
									found_match = True
									found_path = new_path
					paths = new_paths
				if found_match:
					# print(f'Found match of ({found_path.get_origin()})')
					# print(f'Found path is {found_path}')
					match_data = [current_label] 	# [label, (current position), (neighbor position)]
					match_data.append((found_path.get_origin()[0], found_path.get_origin()[1]))
					match_data.append((found_path.get_terminal()[0], found_path.get_terminal()[1]))
					match_data.append(found_path.get_middle_path())
					break
		return match_data

	@classmethod
	def find_growable_cells(cls, padded_cells, cell_location, target_label):
		neighbors = []
		growable_cells = []
		neighbors.append((cell_location[0]-1, cell_location[1]))
		neighbors.append((cell_location[0]+1, cell_location[1]))
		neighbors.append((cell_location[0], cell_location[1]-1))
		neighbors.append((cell_location[0], cell_location[1]+1))
		for neighbor in neighbors:
			# if neighbor is in panel
			if (neighbor[0] >= 0) and (neighbor[0] < len(padded_cells)):
				if (neighbor[1] >= 0) and (neighbor[1] < len(padded_cells[1])):
					current_label = padded_cells[neighbor[0]][neighbor[1]]
					if (current_label == 0) or (current_label == target_label):
						growable_cells.append(neighbor)
		if len(growable_cells) > 0:
			return growable_cells
		else:
			return False