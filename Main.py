import pygame as pg
from pygame.locals import *
from Settings import *

from os import environ
from sys import exit
from math import hypot

import Level as lvl
import Object as obj
import UI

environ['SDL_VIDEO_WINDOW_CENTRED'] = "true"

class Main:
	def __init__(self):		
		pg.init()
		GAME["screen"] = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), HWSURFACE|DOUBLEBUF)

		self.running = True
		self.clock = pg.time.Clock()
		self.disapear = False

		obj.level = lvl.Level("level 3")
		obj.level.decipher_level()
		obj.level.sprites()
		obj.level.connect_objects()

		for i in range(5):
			UI.Heart(i)
		UI.Coin()
		UI.Hover_Message()

	def events(self):
		for event in pg.event.get():
			if event.type == QUIT:
				pg.quit()
				exit()
				self.running = False

	def update(self):
		
		SCROLL[0] += int((obj.PLAYER.rect.x-SCROLL[0]-WIN_WIDTH/2+obj.PLAYER.image.get_width()/2)/6)
		SCROLL[1] += int((obj.PLAYER.rect.y-SCROLL[1]-WIN_HEIGHT/2+obj.PLAYER.image.get_height()/2)/6)

		obj.SPRITES.update()
		obj.UI.update()
		obj.PARTICLES.update()

	def redraw(self):
		GAME["screen"].fill(BACKGROUND_COLOR)

		for light in obj.LIGHT:
			light.draw()
		
		if self.disapear and not obj.PLAYER.effects["night vision"][0]:
			for spr in obj.SPRITES:
				for lht in obj.LIGHT:

					x = spr.rect.center[0]-lht.loc[0]
					if x > 0: x -= TILE_SIZE/2
					else: x += TILE_SIZE/2

					y = spr.rect.center[1]-lht.loc[1]
					if y > 0: y -= TILE_SIZE/2
					else: y += TILE_SIZE/2

					if hypot(x, y) < lht.time*2:
						GAME["screen"].blit(spr.image, (spr.rect.x-SCROLL[0], spr.rect.y-SCROLL[1]))
		
		else:
			for spr in obj.SPRITES:
				GAME["screen"].blit(spr.image, (spr.rect.x-SCROLL[0], spr.rect.y-SCROLL[1]))

		for particle in obj.PARTICLE:
			particle.draw()

		for entity in obj.ENTITY:
			GAME["screen"].blit(entity.image, (entity.rect.x-SCROLL[0], entity.rect.y-SCROLL[1]))

		for lht_prt in obj.LIGHT_PARTICKLES:
			lht_prt.draw()

		for ui in obj.UI:
			GAME["screen"].blit(ui.image, ui.rect.topleft)

		pg.display.flip()
		pg.display.set_caption(f"{self.clock.get_fps():.2f}")

	def main_loop(self):
		while self.running:
			self.events()
			self.update()
			self.redraw()
			self.clock.tick(60)


if __name__ == '__main__':
	main = Main()
	main.main_loop()