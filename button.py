import pygame

pygame.font.init()
font_consola = pygame.font.Font('./CONSOLA.TTF', 12)

class Button:
	def __init__(self, rect=[0, 0, 60, 30], border_radius=3, is_active=True, active_color=(100, 100, 200),
		passive_color=(100, 100, 100), text="Button", font=font_consola, text_color=(255, 255, 255)):
		self.__rect = pygame.Rect(*rect)
		self.__border_radius = border_radius
		self.__active_color = active_color
		self.__passive_color = passive_color
		self.__is_active = True
		self.__text_surface = font.render(text, True, text_color)

	### getter ----------------------------------------------------------------------------------
	def get_is_active(self):
		return self.__is_active

	### setter ----------------------------------------------------------------------------------
	def set_is_active(self, is_active):
		self.__is_active = is_active

	def set_topleft(self, topleft):
		self.__rect.topleft = topleft

	# draw button with text
	def draw(self, display):
		if self.__is_active:
			background_color = self.__active_color
		else:
			background_color = self.__passive_color

		# draw button background and border
		pygame.draw.rect(display, background_color, self.__rect, width=0, border_radius=self.__border_radius)

		# draw text on center of button
		padding_x = (self.__rect.width - self.__text_surface.get_size()[0])/2
		padding_y = (self.__rect.height - self.__text_surface.get_size()[1])/2
		display.blit(self.__text_surface, (self.__rect.x + padding_x, self.__rect.y+padding_y))

	# return True when button is clicked by left mouse button
	def check_click(self, event):
		x, y = pygame.mouse.get_pos()
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed()[0]:		# left mouse clicked
				if self.__rect.collidepoint(x, y):
					self.__is_active = not self.__is_active
					return True
		return False