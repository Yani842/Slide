import pygame as pg
from pygame.locals import *
from Settings import *

from math import ceil
import Particles as prt
import Object as ent

vec = pg.math.Vector2


class Wall(pg.sprite.DirtySprite):
	def __init__(self, loc, groups):
		pg.sprite.DirtySprite.__init__(self, groups)
		self.type = "wall"
		self.loc = loc
		self.pos = vec(loc) * TILE_SIZE


class Frozen(Wall):
	def __init__(self, loc, groups):
		Wall.__init__(self, loc, groups)
		self.subtype = "frozen"


class Sandy(Wall):
	def __init__(self, loc, groups):
		Wall.__init__(self, loc, groups)
		self.subtype = "sandy"


class Harmful(Wall):
	def __init__(self, loc, groups):
		Wall.__init__(self, loc, groups)
		self.subtype = "harmful"
		self.harm = "harmful wall"


class Glow(Wall):
	def __init__(self, loc, groups):
		Wall.__init__(self, loc, groups)
		self.subtype = "glow"
		self.radius = 0
		self.dest_radius = 0
		self.timer = 0

	def update(self):
		self.rect = self.rect.inflate(2, 2)
		hit = pg.sprite.collide_rect(self, ent.PLAYER)
		self.rect = self.rect.inflate(-2, -2)
		
		if hit: self.dest_radius, self.timer = 30, 120
		if self.dest_radius < self.radius: self.radius -= 1
		if self.dest_radius > self.radius: self.radius += 1
		if self.timer <= 0: self.dest_radius = 0
		self.timer -= 1
				
		if self.radius > 0: prt.Light((self.rect.center[0], self.rect.center[1]), self.radius, False, (30, 30, 30), "square")
