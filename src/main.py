import pygame
import sys
import random
import time
import json

pygame.init()

game_title = "Bouncy shot"
ORIGINAL_WINDOW_SIZE = (650, 430)
window = pygame.display.set_mode(ORIGINAL_WINDOW_SIZE)
pygame.display.set_caption(game_title)

game_surface = pygame.Surface(ORIGINAL_WINDOW_SIZE)

game_clock = pygame.time.Clock()
fps = 60

game_mode = 0 #0-menu, 1-game

dark_blue = (14, 29, 54)
red = (217, 4, 29)
white = (255, 255, 255)

point_of_no_return = 400

difficulties = ['easy', 'medium', 'hard']

def collision_sound_effect():
	sound_effect = pygame.mixer.Sound(r'other\collision.wav')
	pygame.mixer.Sound.play(sound_effect)

def load_game_difficulty():
	with open(r'other\game_data.json', 'r') as file:
		data = json.load(file)

		game_difficulty = data['difficulty']

		return game_difficulty

def change_num_of_enemies(): #put in settings loop
	global num_of_enemeis

	if load_game_difficulty() == difficulties[0]:
		num_of_enemies = random.randint(2, 3)
	elif load_game_difficulty() == difficulties[1]:
		num_of_enemies = random.randint(4, 6)
	else: 
		num_of_enemies = random.randint(5, 7)

	return num_of_enemies

num_of_enemies = change_num_of_enemies()
enemies = []

font_path = r'other\earz.ttf'
def render_text(font_path, size, text_to_render, anti_aliased, color, pos):
	font = pygame.font.Font(font_path, size)
	text = font.render(text_to_render, anti_aliased, color)
	text_rect = pygame.Rect(text.get_size()[0], text.get_size()[1], pos[0], pos[1])

	game_surface.blit(text, pos)

	return text_rect

class Ball():
	def __init__(self):
		self.size = [50, 50]
		self.surf = pygame.Surface(self.size)
		self.surf.set_colorkey((0,0,0))
		self.rect = self.surf.get_rect(x=300, y=380)

		self.previous_frame = time.time()

		self.points = 0

	def bounce(self, move):
		self.rect.y += move

		if self.rect.y >= 350:
			self.rect.y -= 130

	def update(self):
		window_width, window_height = pygame.display.get_surface().get_size()
		game_surface.blit(self.surf, self.rect)
		pygame.draw.circle(self.surf, white, (self.size[0] / 2, self.size[0] / 2), 25)

		now = time.time()
		delta_time = now - self.previous_frame
		self.previous_frame = now

		move = 250 * delta_time

		key = pygame.key.get_pressed()

		if key[pygame.K_d] and self.rect.x < window_width - self.size[0]: 
			self.rect.x += move
		elif key[pygame.K_a] and self.rect.x > 0: 
			self.rect.x -= move

		self.bounce(move)

player = Ball()

class Enemy():
	def __init__(self):
		self.random_size = random.randint(45, 55)
		self.size = [self.random_size, self.random_size]
		self.surf = pygame.Surface(self.size)
		self.surf.set_colorkey((0,0,0))

		self.window_width, self.window_height = pygame.display.get_surface().get_size()
		self.rect = self.surf.get_rect(x=random.randint(0, self.window_width - 100), y=random.randint(-10, 0))

		self.previous_frame = time.time()

	def update(self):
		global game_mode

		game_surface.blit(self.surf, self.rect)
		pygame.draw.circle(self.surf, red, (self.size[0] / 2, self.size[0] / 2), 25)

		now = time.time()
		delta_time = now - self.previous_frame
		self.previous_frame = now

		move = 185 * delta_time

		self.rect.y += move

		if self.rect.y > point_of_no_return:
			game_mode = 0

		if self.rect.colliderect(player.rect):
			collision_sound_effect()
			self.rect.x = random.randint(0, window_width - 100)
			self.rect.y = random.randint(-10, 0)
			self.random_size = random.randint(45, 55)
			player.points += 1

for e in range(num_of_enemies):
	enemies.insert(e, Enemy())

def resize_window_contents():
	window_width, window_height = pygame.display.get_surface().get_size()

	new_surf = pygame.transform.scale(game_surface, (window_width, window_height))

	window.blit(new_surf, (0,0))

while game_mode == 0:
	mx, my = pygame.mouse.get_pos()
	window_width, window_height = pygame.display.get_surface().get_size()
	for enemy in enemies:
		enemy.rect.x = random.randint(0, window_width - 100)
		enemy.rect.y = random.randint(-10, 0)
	player.points = 0

	game_surface.fill(dark_blue)

	render_text(font_path, 40, "BOUNCY", False, white, [230, 100])
	render_text(font_path, 40, "SHOTS", False, red, [240, 130])
	render_text(font_path, 15, "(C) 2021, Abigail Adegbiji", False, white, [190, 400])

	play = render_text(font_path, 25, "PLAY", False, white, [280, 260])

	if play.collidepoint(mx, my) and pygame.mouse.get_pressed()[0]:
		game_mode = 1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	resize_window_contents()
	pygame.display.update()
	game_clock.tick(fps)

	while game_mode == 1:
		window_width, window_height = pygame.display.get_surface().get_size()
		game_surface.fill(dark_blue)
		render_text(font_path, 35, f'{player.points}', False, white, (0,0))
		player.update()
		pygame.draw.line(game_surface, white, (0, point_of_no_return),(window_width,point_of_no_return))

		for enemy in enemies:
			enemy.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		resize_window_contents()
		pygame.display.update()
		game_clock.tick(fps)