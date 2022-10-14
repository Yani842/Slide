import pygame as pg
from pygame.locals import *
from Settings import *

from math import hypot, atan2, pi, cos, sin
import random as rd

import UI
import Object as ent
import Particles as prt

vec = pg.math.Vector2


class Enemy(pg.sprite.DirtySprite):
	def __init__(self, loc, groups):
		pg.sprite.DirtySprite.__init__(self, groups)
		self.type = "enemy"
		self.harm = "enemy"
		self.loc = loc
		self.pos = vec(loc) * TILE_SIZE
		self.vel = vec(0, 0)
		self.speed = 0.5

		self.lock = False
		self.life = 16
		self.max_life = 16
		self.ent_messeges = []
		self.life_bar = UI.Life_Bar(self)

		self.counter = {"hurt freq": [False, 0, 3]}


	def die(self):
		change_animation(self, "death", "normal")
		self.lock = True

		for msg in self.ent_messeges:
			msg.disapear = True
			msg.appear = False

		if does_go_animation_end(self, "death", "normal"):
			self.kill()

		pos_x = rd.randint(self.rect.left, self.rect.right)
		pos_y = rd.randint(self.rect.top, self.rect.bottom)
		prt.Particle([pos_x, pos_y], [0, 0], rd.randint(4, 7), False, (110, 200, 150))


	def hurt(self, damage):
		self.life -= damage

		for msg in self.ent_messeges:
			msg.advance_in_queue()
		
		self.ent_messeges.append(UI.Entity_Message(self, self.rect.right, self.rect.top, f"-{damage}", False))


	def collide(self, dir):
		if dir == 'x':
			hits = pg.sprite.spritecollide(self, ent.ENTITY_COLLIDED, False)
			if hits and hits[0].type != "enemy":
				if self.vel.x > 0:
					self.pos.x = hits[0].rect.left - self.rect.width
					self.vel.x = 0

				if self.vel.x < 0:
					self.pos.x = hits[0].rect.right
					self.vel.x = 0

				self.rect.x = self.pos.x

		if dir == 'y':
			hits = pg.sprite.spritecollide(self, ent.ENTITY_COLLIDED, False)
			if hits and hits[0].type != "enemy":
				if self.vel.y > 0:
					self.pos.y = hits[0].rect.top - self.rect.height
					self.vel.y = 0
					
				if self.vel.y < 0:
					self.pos.y = hits[0].rect.bottom
					self.vel.y = 0
					
				self.rect.y = self.pos.y

	
	def get_friction(self):
		frictions = []
		
		self.rect = self.rect.inflate(2, 2)
		hits = pg.sprite.spritecollide(self, ent.PLAYER_FRIC_INFLUES, False)
		self.rect = self.rect.inflate(-2, -2)

		if hits:
			for obj in hits:
				frictions.append(PLAYER_FRICTION[obj.type][obj.subtype])

			total = sum(set(frictions))

		else: total = PLAYER_FRICTION["normal"]

		return total

	def harmful_collide(self):
		if self.counter["hurt freq"][0]:
			
			self.rect = self.rect.inflate(3, 3)
			hits = pg.sprite.spritecollide(self, ent.ENTITY_HARMFUL, False)
			self.rect = self.rect.inflate(-3, -3)
			
			if hits:
				if not self.animation_control["death"]["normal"][0]:
					change_animation(self, "idle", "injured")

				for k, v in ENEMY_DAMAGE.items():
					if any([True for x in hits if x.harm == k]): self.hurt(v)
			
			else:
				if self.animation_control["idle"]["injured"][0]:
					change_animation(self, "idle", "normal")


	def special_collide(self):
		hits = pg.sprite.spritecollide(self, ent.SPECIALS, False)
		for hit in hits:

			if hit.type == "portal":
				self.pos = pg.math.Vector2(hit.get_dist()) * TILE_SIZE

			elif hit.type == "trigger":
				hit.press()

			elif hit.type == "river":
				self.life = 0

		hits = pg.sprite.spritecollide(self, ent.BULLET, False)

		if hits and any([x.do_hurt() for x in hits]):
			self.hurt(4)


	def movement(self):
		self.acc = vec(0, 0)

		x1, y1 = self.rect.center
		x2, y2 = ent.PLAYER.rect.center
		dx, dy = x2 - x1, y2 - y1

		if hypot(dx, dy) < TILE_SIZE * 7:
				
			rads = atan2(dy, dx)
			rads %= 2 * pi

			self.acc.x = (self.speed*cos(rads))
			self.acc.y = (self.speed*sin(rads))

		if self.lock:
			self.acc = vec(0, 0)

		self.acc.x += self.vel.x * self.get_friction()
		self.acc.y += self.vel.y * self.get_friction()

		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc

		self.rect.x = self.pos.x
		self.collide("x")
		self.rect.y = self.pos.y
		self.collide("y")

		if vec(int(self.vel.x), int(self.vel.y)) != vec(0, 0):
			pos_x = rd.randint(self.rect.left, self.rect.right)
			pos_y = rd.randint(self.rect.top, self.rect.bottom)

			prt.Particle([pos_x, pos_y], [0, 0], rd.randint(2, 4), False, (161, 230, 171))


	def update(self):
		for name, count in self.counter.items():
			count[1] += 0.1
			if count[1]//1 == count[2]:
				count[1], count[0] = 0, True
			else: count[0] = False

		if ent.PLAYER.life > 0: self.movement()
		self.harmful_collide()
		self.special_collide()
		animation_update(self)

		if self.life <= 0 or self.lock:
			self.die()
