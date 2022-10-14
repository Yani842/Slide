import pygame as pg
from pygame.locals import *

import random as rd
import Settings as stn
import Object as obj
import Particles as prt

vec = pg.math.Vector2

class Bullet(pg.sprite.DirtySprite):
	def __init__(self, pos, groups, dire):
		pg.sprite.DirtySprite.__init__(self, groups)
		self.type = "bullet"
		self.dire = dire # vec(-1/1, -1/1)
		self.pos = pos

		self.exp = False
		self.hurt = True
		self.radius = 0
		self.dest_radius = 15

	def update(self):
		if not self.exp:
			self.pos += self.dire*4
			self.rect.topleft = self.pos

			if self.rect.x-stn.SCROLL[0] > stn.WIN_WIDTH or self.rect.y-stn.SCROLL[1] > stn.WIN_HEIGHT:
				self.kill()
		
			if 0 > self.rect.right-stn.SCROLL[0] or 0 > self.rect.bottom-stn.SCROLL[1]:
				self.kill()
		
		hits = pg.sprite.spritecollide(self, obj.PLAYER_COLLIDED, False)
		if hits or self.exp:
			self.explosion()

		if stn.does_go_animation_end(self, "shoot", "normal") and self.animation_control["idle"]["normal"][1] == 1:
			stn.change_animation(self, "idle", "normal")

		stn.animation_update(self)

		if self.dest_radius < self.radius:
			self.radius -= 2
		if self.dest_radius > self.radius:
			self.radius += 2

		prt.Light((self.rect.center[0], self.rect.center[1]), self.radius, False, (50, 50, 70))


	def do_hurt(self):
		if self.hurt:
			self.hurt = False 
			return True
		return False


	def explosion(self):
		self.exp = True
		self.dest_radius = 0

		stn.change_animation(self, "explosion", "normal")

		if stn.does_go_animation_end(self, "explosion", "normal"):
			self.kill()
