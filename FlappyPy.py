from sys import exit as sys_exit
from os.path import join as os_join
from os import getcwd as os_getcwd
from random import randint

import pygame, pygame.freetype

class Game:
	def __init__(self):
		#Initializing bakend variables and modules
		pygame.init()
		self.display = pygame.display.set_mode((400, 600))
		pygame.display.set_caption('FlappyPy')
		self.font = pygame.freetype.SysFont('Arial', 30)
		self.clock = pygame.time.Clock()
		self.dt = 0
		self.game_state = 0

		# Load or Create highscore file and initialize highscore variables
		try:
			self.highscore_file = open(os_join(os_getcwd(), 'highscore'), 'r+')
			self.highscore = bytes.fromhex(self.highscore_file.read()).decode('utf-8').split('.')[1]
		except:
			highscore_file = open(os_join(os_getcwd(), 'highscore'), 'w+')
			highscore_file.close()
			self.highscore_file = open(os_join(os_getcwd(), 'highscore'), 'r+')
			self.highscore = ''
		self.updated_highscore = False

		# Initialiing frontend variables
		self.player_rect = pygame.Rect(170, 270, 30, 30)
		self.player_velocity = 0
		self.gravity = 10
		self.jump_height = -255
		self.pipes = []
		self.speed = 10
		self.speed_multiplier = 0
		self.score = 0
		self.last_increased_score = 0

	def update(self):
		self.handle_events()

		if self.game_state == 1:
			self.move_pipes()
			self.move_player()

		elif self.game_state == 2:
			if self.highscore != '':
				if int(self.highscore) < self.score:
					self.update_highscore()
			else:
				self.update_highscore()

	def render(self):
		self.display.fill((255, 255, 255))

		if self.game_state == 0:
			self.font.render_to(self.display, (60, 200), 'Press any key to start!', (0, 0, 0))
			self.font.render_to(self.display, (75, 300), 'Press Space to flap', (0, 0, 0))

		elif self.game_state == 1:
			for pipe in self.pipes:
				pygame.draw.rect(self.display, (0, 255, 0), pipe[0])
				pygame.draw.rect(self.display, (0, 255, 0), pipe[1])
			pygame.draw.rect(self.display, (255, 255, 0), self.player_rect)
			self.font.render_to(self.display, (20, 10), str(self.score), (0, 0, 0))

		elif self.game_state == 2:
			if self.highscore != '':
				if int(self.highscore) >= self.score and not self.updated_highscore:
					self.font.render_to(self.display, (100, 200), 'Final Score: ' + str(self.score), (0, 0, 0))
					self.font.render_to(self.display, (110, 300), 'Highscore: ' + self.highscore, (0, 0, 0))
				else:
					self.font.render_to(self.display, (90, 200), 'New Highscore: ' + str(self.score), (0, 0, 0))
			else:
				self.font.render_to(self.display, (90, 200), 'New Highscore: ' + str(self.score), (0, 0, 0))

		pygame.display.flip()

	def run(self):
		self.new_game()
		while True:
			self.update()
			self.render()
			self.dt = self.clock.tick(60) / 1000

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.highscore_file.close()
				pygame.quit
				sys_exit()
			elif event.type == pygame.KEYDOWN:
				if self.game_state == 0:
					self.game_state = 1
				elif self.game_state == 1:
					if event.key == pygame.key.key_code('space'):
						self.jump()
				elif self.game_state == 2:
					if event.key != pygame.key.key_code('space'):
						self.new_game()
						self.game_state = 1

	def move_pipes(self):
		# Interate through pipes to move them and check positions for various game functions
		for pipe in self.pipes:
			pipe[0].x -= self.speed * self.speed_multiplier * self.dt
			pipe[1].x -= self.speed * self.speed_multiplier * self.dt
			# Check if pipe has moved far enough left to add to the score
			if pipe[0].x < 150 and not pipe[2]:
				self.add_score()
				pipe[2] = True

			# Check if pipe has moved far enough left to spawn another pipe
			if pipe[0].x < 200 and not pipe[3]:
				self.add_pipe()
				pipe[3] = True

			# Check if player has collided with pipe
			if self.player_rect.colliderect(pipe[0]) or self.player_rect.colliderect(pipe[1]):
				self.updated_highscore = False
				self.game_state = 2
				break

		# Interate through pipes too delete the ones that have reached the left edge
		for i in range(len(self.pipes)):
			if self.pipes[i][0].x <= 0: self.pipes.pop(i)
			break

	def move_player(self):
		# Add to player velocity to simulate gravity and then add to the player 'y' position to move the player
		self.player_velocity += self.gravity
		self.player_rect.y += self.player_velocity * self.dt

		# Check if the player has left the screen
		if self.player_rect.y < 0 or self.player_rect.y > 570:
			self.updated_highscore = False
			self.game_state = 2

	def jump(self):
		self.player_velocity = self.jump_height

	def add_pipe(self):
		# Generate a 'y' position offset for the pipes and append a new pipe to the array
		offset = randint(100, 500)
		self.pipes.append([pygame.Rect(400, -600 + offset, 20, 600), pygame.Rect(400, 100 + offset, 20, 600), False, False])

	def add_score(self):
		self.score += 1
		if self.score == self.last_increased_score + 4:
			self.last_increased_score = self.score
			self.speed_multiplier += 1

	def new_game(self):
		self.player_rect.y = 270
		self.player_velocity = 0
		self.pipes = []
		self.speed_multiplier = 1
		self.score = 0
		self.last_increased_score = 0
		self.add_pipe()

	def update_highscore(self):
		if not self.updated_highscore:
			self.highscore_file.seek(0)
			self.highscore_file.write(('jacob.' + str(self.score) + '.maughan').encode('utf-8').hex())
			self.highscore_file.truncate()
			self.highscore = str(self.score)
			self.updated_highscore = True

if __name__ == '__main__':
	game = Game()
	game.run()