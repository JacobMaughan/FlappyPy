from sys import exit as sys_exit
from os.path import join as os_join
from os import getcwd as os_getcwd
from random import randrange

import pygame, pygame.freetype

class Game:
	def __init__(self):
		pygame.init()
		self.display = pygame.display.set_mode((400, 600))
		pygame.display.set_caption('FlappyPy')

		self.clock = pygame.time.Clock()
		self.font = pygame.freetype.SysFont('Arial', 30)
		self.dt = 0

		self.state = 0
		
		self.score = 0
		self.pipes = []
		self.pipe_speed_multiplier = 1
		self.last_score_sped_up = 0

		self.player_rect = pygame.Rect(170, 270, 30, 30)
		self.player_vel = 0

		try:
			self.highscore_file = open(os_join(os_getcwd(), 'highscore'), 'r+')
			self.highscore = bytes.fromhex(self.highscore_file.read()).decode('utf-8').split('.')[1]
		except:
			highscore_file = open(os_join(os_getcwd(), 'highscore'), 'w+')
			highscore_file.close()
			self.highscore_file = open(os_join(os_getcwd(), 'highscore'), 'r+')
			self.highscore = ''
		self.updated_highscore = False

		self.add_pipe()

	def run(self):
		while True:
			self.get_event()
			if self.state == 1:
				self.update()
			self.draw()
			self.dt = self.clock.tick(60) / 1000

	def update(self):
		if self.score == self.last_score_sped_up + 4:
			self.last_score_sped_up = self.score
			self.pipe_speed_multiplier += 1
		for pipe in self.pipes:
			pipe[0].x -= 10 * self.pipe_speed_multiplier * self.dt
			pipe[1].x -= 10 * self.pipe_speed_multiplier * self.dt
			if pipe[0].x < 150 and not pipe[2]:
				self.score += 1
				pipe[2] = True
			if pipe[0].x < 200 and not pipe[3]:
				self.add_pipe()
				pipe[3] = True
			if self.player_rect.colliderect(pipe[0]) or self.player_rect.colliderect(pipe[1]):
				self.state = 2
				self.updated_highscore = False
				break
		for i in range(len(self.pipes)):
			if self.pipes[i][0].x <= 0: self.pipes.pop(i)
			break
		self.player_vel += 10
		self.player_rect.y += self.player_vel * self.dt
		if self.player_rect.y < 0 or self.player_rect.y > 570:
			self.state = 2
			self.updated_highscore = False

	def draw(self):
		if self.state == 0:
			self.display.fill((255, 255, 255))
			self.font.render_to(self.display, (60, 200), 'Press any key to start!', (0, 0, 0))
			self.font.render_to(self.display, (75, 300), 'Press Space to flap', (0, 0, 0))
			pygame.display.flip()
		elif self.state == 1:
			self.display.fill((255, 255, 255))
			for pipe in self.pipes:
				pygame.draw.rect(self.display, (0, 255, 0), pipe[0])
				pygame.draw.rect(self.display, (0, 255, 0), pipe[1])
			pygame.draw.rect(self.display, (255, 255, 0), self.player_rect)
			self.font.render_to(self.display, (20, 10), str(self.score), (0, 0, 0))
			pygame.display.flip()
		elif self.state == 2:
			self.display.fill((255, 255, 255))
			if self.highscore != '':
				if int(self.highscore) >= self.score and not self.updated_highscore:
					self.font.render_to(self.display, (100, 200), 'Final Score: ' + str(self.score), (0, 0, 0))
					self.font.render_to(self.display, (110, 300), 'Highscore: ' + self.highscore, (0, 0, 0))
				else:
					self.font.render_to(self.display, (90, 200), 'New Highscore: ' + str(self.score), (0, 0, 0))
					if not self.updated_highscore:
						self.highscore_file.seek(0)
						self.highscore_file.write(('flappy.' + str(self.score) + '.py').encode('utf-8').hex())
						self.highscore_file.truncate()
						self.highscore = str(self.score)
						self.updated_highscore = True
			else:
				self.font.render_to(self.display, (90, 200), 'New Highscore: ' + str(self.score), (0, 0, 0))
				if not self.updated_highscore:
					self.highscore_file.seek(0)
					self.highscore_file.write(('flappypy.' + str(self.score) + '.py').encode('utf-8').hex())
					self.highscore_file.truncate()
					self.highscore = str(self.score)
					self.updated_highscore = True
			pygame.display.flip()

	def get_event(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.highscore_file.close()
				pygame.quit()
				sys_exit()
			elif event.type == pygame.KEYDOWN:
				if self.state == 0:
					self.state = 1
				elif self.state == 1:
					if event.key == pygame.key.key_code('space'):
						self.player_vel = -225
				elif self.state == 2:
					if event.key != pygame.key.key_code('space'):
						self.score = 0
						self.pipes = []
						self.player_rect.y = 270
						self.player_vel = 0
						self.add_pipe()
						self.state = 1

	def add_pipe(self):
		offset = randrange(100, 500)
		self.pipes.append([pygame.Rect(400, -600 + offset, 20, 600), pygame.Rect(400, 100 + offset, 20, 600), False, False])