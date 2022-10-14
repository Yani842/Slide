import pygame as pg
from pygame.locals import *
from Settings import *
import Settings as stn
import Object as ent
import random as rd


class Portal(pg.sprite.DirtySprite):
	def __init__(self, loc, groups, dist):
		pg.sprite.DirtySprite.__init__(self, groups)
		self.type = "portal"
		self.loc = loc
		self.dist = dist
		self.pos = vec(loc) * TILE_SIZE
	
	def update(self):
		animation_update(self)
	
	def get_dist(self):

		change_animation(self, "enter", "normal")

		return rd.choice(self.dist)


class River(pg.sprite.DirtySprite):
	def __init__(self, loc, groups):
		pg.sprite.DirtySprite.__init__(self, groups)
		self.type = "river"
		self.loc = loc
		self.dire = "M"
		self.pos = vec(loc) * TILE_SIZE
	
	def update(self):
		animation_update(self)

	def set_dire(self, dire):

		self.dire = ""

		if dire["up"]: self.dire += "U"
		if dire["down"]: self.dire += "D"
		if dire["left"]: self.dire += "L"
		if dire["right"]: self.dire += "R"
		if dire["middle"]: self.dire += "M"

		change_animation(self, self.dire, "normal")


class Trigger(pg.sprite.DirtySprite):
	def __init__(self, loc, groups):
		pg.sprite.DirtySprite.__init__(self, groups)
		self.type = "trigger"
		self.loc = loc
		self.pos = vec(loc) * TILE_SIZE
		self.timer = 0

	def press(self):
		if not self.timer:
			self.timer = 1

	def update(self):
		if self.timer:
			self.timer += 1

			if self.timer == 90:

				stn.level.load_object(rvr := River(self.loc, ent.groups["river"]))
				stn.level.sprites(rvr)
				stn.level.connect_objects()
				self.kill()


class Box(pg.sprite.DirtySprite):
	def __init__(self, loc, groups, inventory = {}):
		pg.sprite.DirtySprite.__init__(self, groups)
		self.type = "trigger"
		self.loc = loc
		self.pos = vec(loc) * TILE_SIZE
		self.inventory = inventory

	def update(self):
		animation_update(self)