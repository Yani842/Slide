import pygame as pg
from pygame.locals import *
from Settings import *

vec = pg.math.Vector2

class Item(pg.sprite.DirtySprite):
	def __init__(self, loc, groups):
		pg.sprite.DirtySprite.__init__(self, groups)
		self.type = "item"
		self.loc = loc
		self.pos = vec(loc) * TILE_SIZE

	def collect(self):
		self.kill()


class Coin(Item):
	def __init__(self, loc, groups, value):
		Item.__init__(self, loc, groups)
		self.subtype = "coin"
		self.value = value

	def update(self):
		self.animation_control[str(self.value)]["normal"][0] = True
		animation_update(self)


class Rune(Item):
	def __init__(self, loc, groups, effect):
		Item.__init__(self, loc, groups)
		self.subtype = "rune"
		self.effect = effect

	def update(self):
		self.animation_control[self.effect]["normal"][0] = True
		animation_update(self)


class Light_Piece(Item):
	def __init__(self, loc, groups, value):
		Item.__init__(self, loc, groups)
		self.subtype = "light piece"
		self.value = value

	def update(self):
		animation_update(self)