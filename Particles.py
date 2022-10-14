import pygame as pg
from pygame import gfxdraw
from pygame.locals import *
from Settings import *
import Object as obj

def circle_surf(radius, color):
	surf = pg.Surface((radius * 2, radius * 2))
	pg.draw.circle(surf, color, (radius, radius), radius)
	surf.set_colorkey((0, 0, 0))
	return surf

def square_surf(width, color):
	surf = pg.Surface((width * 2, width * 2))
	pg.draw.rect(surf, color, surf.get_rect(), border_radius=int(width//8))
	surf.set_colorkey((0, 0, 0))
	return surf

def translate_arg(arg):
	if arg[0] == "randint":
		return rd.randint(arg[1])

	elif arg[0] == "uniform":
		return rd.uniform(arg[1])

	else:
		return arg

""""player die": {
		"velocity": [0, 0],
		"time": ["randint", [4, 7]],
		"size": {
			"do equal to time": true,
			"subtract": 0
		},
		"grav": {
			"do grav": false,
			"velocity": [0, 0]
		},
		"image": {
			"type": "shape",
			"shape": "circle",
			"color": [200, 100, 106],
			"image path": ["..."],
			"image set path": ["...(folder)"]
		}
	}"""

class Particle(pg.sprite.DirtySprite):
	def __init__(self, loc, velocity, time, do_grav, color):
		pg.sprite.DirtySprite.__init__(self, [obj.PARTICLE, obj.PARTICLES])
		self.loc = loc
		self.vel = velocity
		self.time = time
		self.do_grav = do_grav
		self.color = color
		#self.vel = (translate_arg(args["velocity"][0]), translate_arg(args["velocity"][1]))
		#self.time = translate_arg(args["time"])
		#self.size = if args["size"]["do w"]

	def update(self):
		self.loc[0] += self.vel[0]
		self.loc[1] += self.vel[1]
		self.time -= 0.1

		if self.do_grav: self.vel[1] += 0.03

	def draw(self):
		pg.draw.circle(GAME["screen"], self.color, [int(self.loc[0]-SCROLL[0]), int(self.loc[1]-SCROLL[1])], int(self.time))

		if self.time <= 0: self.kill()


class Light_Particle(pg.sprite.DirtySprite):
	def __init__(self, loc, velocity, time, do_grav, color):
		pg.sprite.DirtySprite.__init__(self, [obj.PARTICLE, obj.LIGHT_PARTICKLES])
		self.loc = loc
		self.vel = velocity
		self.time = time
		self.do_grav = do_grav
		self.color = color

	def update(self):
		self.loc[0] += self.vel[0]
		self.loc[1] += self.vel[1]
		self.time -= 0.1

		if self.do_grav: self.vel[1] += 0.03

	def draw(self):
		pg.draw.circle(GAME["screen"], self.color, [int(self.loc[0]-SCROLL[0]), int(self.loc[1]-SCROLL[1])], int(self.time))

		radius = self.time * 2
		GAME["screen"].blit(circle_surf(radius, self.color), (int(self.loc[0] - radius - SCROLL[0]), int(self.loc[1] - radius - SCROLL[1])), special_flags=BLEND_RGBA_ADD)
		
		if self.time <= 0 or not self.do_time: self.do_kill = True


class Light(pg.sprite.DirtySprite):
	def __init__(self, loc, time, do_time, color, shape="circle"):
		pg.sprite.DirtySprite.__init__(self, [obj.LIGHT, obj.PARTICLES])
		self.loc = loc
		self.time = time
		self.do_time = do_time
		self.color = color
		self.do_kill = False
		self.shape = shape

	def update(self):
		if self.do_time: self.time -= 0.1
		if self.do_kill: self.kill()

	def draw(self):
		radius = self.time * 2
		if self.shape == "circle": GAME["screen"].blit(circle_surf(radius, self.color), (int(self.loc[0] - radius - SCROLL[0]), int(self.loc[1] - radius - SCROLL[1])), special_flags=BLEND_RGB_ADD)
		elif self.shape == "square": GAME["screen"].blit(square_surf(radius, self.color), (int(self.loc[0] - radius - SCROLL[0]), int(self.loc[1] - radius - SCROLL[1])), special_flags=BLEND_RGB_ADD)
		if self.time <= 0 or not self.do_time: self.do_kill = True


if __name__ == '__main__': # only for dev
	import Main as m
	main = m.Main()
	main.main_loop()