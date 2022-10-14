import pygame as pg
from pygame.locals import *
import os.path as op
import os

GAME = {"screen":None, "clock":None}

TILE_SIZE = 24
FPS = 60
WIN_HEIGHT = 600
WIN_WIDTH = 800
BACKGROUND_COLOR = (0, 0, 0)
SCROLL = [0, 0]
vec = pg.math.Vector2

PLAYER_ACC = 0.7
PLAYER_FRICTION = {
    "normal": -0.12,
    "wall": {
        "frozen": -0.06,
        "sandy": -0.24
    },
    "obstacle": {
        "jeli": -0.02,
        "tar": -0.45,
        "poisoned": -0.6 
    }
}
EFFECTS_LONG = {"curing":5*FPS, "protection":8*FPS, "obstacles protection":6*FPS, "night vision":5*FPS, "poison": 4*FPS}
PLAYER_DAMAGE = {"harmful wall":3, "enemy":2, "poisoned":3}
ENEMY_DAMAGE = {"harmful wall":1}

images_folder = None
level = None
metadata = {}


def get_size(self):
	if self.type == "item": return 16
	elif self.type == "entity": return 22
	else: return 24

def does_go_animation_end(self, animation, status):
	if int(self.animation_control[animation][status][1]+self.animation_prop[animation][status][1]) >= len(self.animation_control[animation][status][2])+1:
		self.animation_control[animation][status][1] = len(self.animation_control[animation][status][2])
		return True
	else: return False


def change_animation(self, animation_, status_):
	for name, status in self.animation_control.items():
		for status, prop in status.items():
				
			if name == animation_ and status == status_:
				prop[0] = True

			else:
				prop[0] = False


def set_animation(self, prop):

	self.animation_control = {}
	self.animation_prop = {}

	for anim, status in prop.items():

		self.animation_control[anim] = {}
		self.animation_prop[anim] = {}

		for status, prop in status.items():

			if prop[3] == "first":
				self.animation_control[anim][status] = [True, 1, {}]
			elif prop[3] == "later":
				self.animation_control[anim][status] = [False, 1, {}]

			self.animation_prop[anim][status] = prop

			path = op.join(images_folder, *prop[0])

			for i in range(len(os.listdir(path))):
				if op.isfile(op.join(path, f"{i+1}.png")):

					self.animation_control[anim][status][2][i+1] = pg.image.load(op.join(path, f"{i+1}.png")).convert_alpha()

	self.image = self.animation_control[anim][status][2][1]
	self.image = pg.transform.scale(self.image, (get_size(self), get_size(self)))
	self.rect = self.image.get_rect()
	self.rect.topleft = self.pos


def set_image(self, image):
	self.image = image
	self.image = pg.transform.scale(self.image, (get_size(self), get_size(self)))
	self.rect = self.image.get_rect()
	self.rect.topleft = self.pos


def animation_update(self):
	for anim, status in self.animation_control.items():
		for status, prop in status.items():
	
			if prop[0]:
	
				prop[1] += self.animation_prop[anim][status][1]
				
				if self.animation_prop[anim][status][2] == "infinite":
					if prop[1] >= len(prop[2])+1:
						prop[1] = 1

				elif self.animation_prop[anim][status][2] == "back and forth":
					if prop[1] >= len(prop[2])+1 or prop[1] <= 1:

						if self.animation_prop[anim][status][1] > 0:
							self.animation_prop[anim][status][1] = -self.animation_prop[anim][status][1]
							prop[1] = len(prop[2])

						elif self.animation_prop[anim][status][1] < 0:
							self.animation_prop[anim][status][1] = -self.animation_prop[anim][status][1]
							prop[0] = False
							prop[1] = 1
							self.animation_control["idle"]["normal"][0] = True

				elif self.animation_prop[anim][status][2] == "back and forth infinite":
					if prop[1] >= len(prop[2])+1 or prop[1] <= 1:

						if self.animation_prop[anim][status][1] > 0:
							self.animation_prop[anim][status][1] = -self.animation_prop[anim][status][1]
							prop[1] = len(prop[2])

						elif self.animation_prop[anim][status][1] < 0:
							self.animation_prop[anim][status][1] = -self.animation_prop[anim][status][1]
							prop[1] = 1

				self.image = prop[2][int(prop[1])]
				self.image = pg.transform.scale(self.image, (get_size(self), get_size(self)))


if __name__ == '__main__': # only for dev
	import Main as m
	main = m.Main()
	main.main_loop()