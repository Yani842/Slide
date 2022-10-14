import pygame as pg
import Settings as st
from Settings import *
import Object as obj
import os.path as op
import random as rd



class Entity_Message(pg.sprite.DirtySprite):
	def __init__(self, entity, x, y, text, color):
		self._layer = 5
		pg.sprite.DirtySprite.__init__(self, [obj.UI, obj.ENTITY_MESSAGES])

		#self.font = pg.font.Font(op.join(op.dirname(__file__), "font", "VT323-Regular.ttf"), 10)
		self.font = pg.font.SysFont("Arial", 10)

		if color:
			self.image = self.font.render(text, False, (0, 255, 0))
		else:
			self.image = self.font.render(text, False, (255, 0, 0))

		self.rect = self.image.get_rect()

		self.x, self.y = 13, 0

		self.alpha = 0
		self.counter = FPS*2
		self.appear = True
		self.disapear = False
		self.move = 0
		self.do_move = 0
		self.entity = entity

	def advance_in_queue(self):
		self.do_move += 1

	def update(self):
		if self.appear:
			self.x -= 1
			self.alpha += 31.875
			self.image.set_alpha(self.alpha)
			if self.x <= 5:
				self.appear = False
				self.alpha = 255

		if self.disapear:
			self.x += 1
			self.image.fill((255, 255, 255, self.alpha), special_flags=pg.BLEND_RGBA_MULT)
			if self.x >= 13:
				self.disapear = False
				self.kill()
			else:
				self.alpha -= self.alpha/(13-self.x)

		if self.do_move:
			self.move += 1
			if self.move == 10:
				self.move = 0
				self.do_move -= 1
			self.y += 1
		
		self.rect.x, self.rect.y = self.entity.rect.right-SCROLL[0] + self.x, self.entity.rect.top-SCROLL[1] + self.y

		self.counter -= 1
		if not self.counter:
			self.disapear = True


class Life_Bar(pg.sprite.DirtySprite):
	def __init__(self, entity):
		pg.sprite.DirtySprite.__init__(self, [obj.UI, obj.LIFE_BAR])
		self.entity = entity
		self.close = 0

	def update(self):
		self.image = pg.Surface((self.entity.rect.width - self.close, 5))
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.entity.rect.left + self.close / 2 - SCROLL[0], self.entity.rect.bottom+5-SCROLL[1])
		self.image.set_colorkey((0, 0, 0))

		pg.draw.rect(self.image, (127, 127, 127), self.image.get_rect(), border_radius=2)
		rect = self.image.get_rect()
		rect.width = (rect.width / self.entity.max_life) * self.entity.life

		if self.entity.life <= 0:
			self.close += 0.6

		if self.rect.width == 0:
			self.kill()

		if self.entity.max_life == self.entity.life: pg.draw.rect(self.image, (255, 0, 0), rect,
			border_radius=2)

		elif self.entity.max_life > self.entity.life: pg.draw.rect(self.image, (255, 0, 0), rect,
			border_top_left_radius=2,
			border_bottom_left_radius=2)


class Heart(pg.sprite.DirtySprite):
	def __init__(self, place):
		self._layer = 5
		pg.sprite.DirtySprite.__init__(self, [obj.UI, obj.HEARTS])

		self.state = "full"
		self.place = place+1
		self.pos = [place*20+10, 5]
		self.color = rd.randint(1, 35)

	def update(self):
		if obj.PLAYER.life >= self.place*4:
			self.state = "full"

		elif obj.PLAYER.life == self.place*4-1:
			self.state = "three quarter"

		elif obj.PLAYER.life == self.place*4-2:
			self.state = "half"

		elif obj.PLAYER.life == self.place*4-3:
			self.state = "quarter"

		else:
			self.state = "empty"

		if self.state != "empty":
			self.image = pg.image.load(op.join(op.dirname(__file__), "src", "hearts", f"heart {self.state} {self.color}.png"))
		
		else:
			self.image = pg.image.load(op.join(op.dirname(__file__), "src", "hearts", f"heart empty.png"))
		
		self.image = pg.transform.scale(self.image, (18, 18))
		self.rect = self.image.get_rect()
		self.rect.topleft = self.pos


class Effect(pg.sprite.DirtySprite):
	def __init__(self, place, effect):
		self._layer = 5
		pg.sprite.DirtySprite.__init__(self, [obj.UI, obj.EFFECTS])

		self.effect = effect
		self.image = pg.image.load(op.join(op.dirname(__file__), "src", "effect icons", f"effect {effect} icon.png"))
		self.image = pg.transform.scale(self.image, (18, 18))
		self.rect = self.image.get_rect()

		self.x, self.y = 0, 10
		self.place = place
		self.alpha = 0
		self.appear = True
		self.disapear = False
		self.move = 0
		self.do_move = 0


	def update(self):
		if self.appear:
			self.y -= 1
			self.alpha += 255/10
			self.image.set_alpha(self.alpha)
			if self.y == 0:
				self.appear = False
				self.alpha = 255

		if self.disapear:
			self.y += 1
			self.image.fill((255, 255, 255, self.alpha), special_flags=pg.BLEND_RGBA_MULT)
			
			if self.y == 30:
				self.disapear = False
				self.kill()
			else:
				self.alpha -= self.alpha/(30-self.y)

		else:
			if obj.PLAYER.effects[self.effect][0]:
				if self.place != obj.PLAYER.effect_order.index(self.effect):
					self.do_move = self.place - obj.PLAYER.effect_order.index(self.effect)
			else:
				self.do_appear = False
				self.disapear = True
				obj.PLAYER.effect_order.remove(self.effect)

		if self.do_move:
			self.move += 1
			self.x -= 1
			if self.move == 20:
				self.do_move -= 1
				self.place -= 1
				self.move = 0
				self.x = 0

		self.rect.topleft = [self.place*20+10+self.x, 55+self.y]


class Coin(pg.sprite.DirtySprite):
	def __init__(self):
		self._layer = 5
		pg.sprite.DirtySprite.__init__(self, [obj.UI])

		self.image = pg.image.load(op.join(op.dirname(__file__), "src", "icons", "coin icon.png"))
		self.image = pg.transform.scale(self.image, (18, 18))
		self.rect = self.image.get_rect()

		self.rect.topleft = (10, 30)

		Coin_Label(self)


class Coin_Label(pg.sprite.DirtySprite):
	def __init__(self, coin):
		self._layer = 5
		pg.sprite.DirtySprite.__init__(self, [obj.UI])

		#self.font = pg.font.Font(op.join(op.dirname(__file__), "font", "VT323-Regular.ttf"), 16)
		self.font = pg.font.SysFont("Arial", 16)
		self.coin = coin
		self.count = 0

		self.image = self.font.render(f"{int(self.count)}", True, (255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.midleft = (self.coin.rect.right+5, self.coin.rect.centery)

	def update(self):
		if self.count < obj.PLAYER.coin_count:
			self.count += 0.25

			self.image = self.font.render(f"{int(self.count)}", True, (255, 255, 255))
			self.rect = self.image.get_rect()
			self.rect.midleft = (self.coin.rect.right+5, self.coin.rect.centery)


class Hover_Message(pg.sprite.DirtySprite):
	def __init__(self):
		self._layer = 6
		pg.sprite.DirtySprite.__init__(self, [obj.UI, obj.HOVER_MESSAGE])

		self.font = pg.font.Font(op.join(op.dirname(__file__), "font", "VT323-Regular.ttf"), 16)
		self.later = 0
		self.final_text = ""
		self.current_effect = ""

	def update(self):
		mpos = pg.mouse.get_pos()
		pos = [mpos[0]+16, mpos[1]]
		self.text = ""

		for effect in obj.EFFECTS:
			if effect.rect.collidepoint(mpos):
				self.text = effect.effect
				
				if self.current_effect != effect.effect:
					self.current_effect = effect.effect
					self.later = 1
				else:
					self.later += 0.75

		self.final_text = self.text[0:int(self.later)]

		
		self.image = self.font.render(self.final_text, True, (255, 255, 255), (127, 127, 127))
		self.rect = self.image.get_rect()
		self.rect.topleft = (pos)



if __name__ == '__main__': # only for dev
	import Main as m
	main = m.Main()
	main.main_loop()