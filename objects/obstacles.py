import pygame as pg
from pygame.locals import *
from Settings import *

vec = pg.math.Vector2

class Obstacle(pg.sprite.DirtySprite):
	def __init__(self, loc, groups):
		pg.sprite.DirtySprite.__init__(self, groups)
		self.type = "obstacle"
		self.loc = loc
		self.pos = vec(loc) * TILE_SIZE


class Jeli(Obstacle):
	def __init__(self, loc, groups):
		Obstacle.__init__(self, loc, groups)
		self.subtype = "jeli"


class Tar(Obstacle):
	def __init__(self, loc, groups):
		Obstacle.__init__(self, loc, groups)
		self.subtype = "tar"


class Poisoned(Obstacle):
	def __init__(self, loc, groups):
		Obstacle.__init__(self, loc, groups)
		self.subtype = "poisoned"
		self.harm = "poisoned"

