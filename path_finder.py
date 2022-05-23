class PathFinder:
	def find_path(self, padded_cells, target_labels):
		pass

	# find cells with same label in four adjacent connectivity
	@classmethod
	def find_adjacent(cls, padded_cells, target_labels):
		print(padded_cells[0][0])
		original_padded_cells = padded_cells.copy()
		limit_x = len(padded_cells) - 2
		limit_y = len(padded_cells[0]) - 2
		for current_x in range(1, limit_x + 1):
			for current_y in range(1, limit_y + 1):
				neighbors_position = []
				neighbors_position.append((current_x - 1, current_y))
				neighbors_position.append((current_x + 1, current_y))
				neighbors_position.append((current_x, current_y - 1))
				neighbors_position.append((current_x, current_y + 1))
				current_label = original_padded_cells[current_x][current_y]
				if current_label != 0:
					for neighbor_position in neighbors_position:
						neighbor_label = original_padded_cells[neighbor_position[0]][neighbor_position[1]]
						if neighbor_label == current_label:
							print(f'Found adjacent at ({current_x}, {current_y})')
							print(f'      adjacent with ({neighbor_position[0]}, {neighbor_position[1]})')
							print(f'      template number is {current_label}')
							match_data = [] 	# [label, (current position), (neighbor position)]
							match_data.append((current_x, current_y))
							match_data.append((neighbor_position[0], neighbor_position[1]))
							return match_data