import pygame as pg
from pygame.locals import *
from Settings import *

import objects.bullets as sh
import Settings as stn
import Particles as prt
import Object as ent
import UI

import random as rd

vec = pg.math.Vector2


class Player(pg.sprite.DirtySprite):
	def __init__(self, loc, groups):
		self._layer = 1
		pg.sprite.DirtySprite.__init__(self, groups)
		self.type = "player"

		self.coin_count = 0
		self.life = 20
		self.max_life = 20
		self.effect_order = []
		self.ent_massages = []

		self.radius = 0
		self.dest_radius = 0
		self.lock = False
		self.vel = vec(0, 0)
		self.loc = loc
		self.pos = vec(loc) * TILE_SIZE

		self.counter = {"hurt freq": [False, 0, 3],
						"cure effe": [False, 0, 5],
						"shut freq": [False, 0, -1]}

		self.effects = {"curing": [False, 0],
						"protection": [False, 0],
						"obstacles protection": [False, 0],
						"night vision": [False, 0]}


	def hurt(self, damage):
		self.life -= damage

		for msg in self.ent_massages:
			msg.advance_in_queue()
		
		self.ent_massages.append(UI.Entity_Message(self, self.rect.right, self.rect.top, f"-{damage}", False))


	def heal(self, strength):
		self.life += strength

		for msg in self.ent_massages:
			msg.advance_in_queue()

		self.ent_massages.append(UI.Entity_Message(self, self.rect.right, self.rect.top, f"+{strength}", True))


	def collide(self, dir):
		if dir == 'x':
			if hits := pg.sprite.spritecollide(self, ent.PLAYER_COLLIDED, False):
				if self.vel.x > 0:
					self.pos.x = hits[0].rect.left - self.rect.width
					self.vel.x = 0

				if self.vel.x < 0:
					self.pos.x = hits[0].rect.right
					self.vel.x = 0

				self.rect.x = self.pos.x

		if dir == 'y':
			if hits := pg.sprite.spritecollide(self, ent.PLAYER_COLLIDED, False):
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

		for obj in hits:
				
			if not (obj.type == "obstacle" and self.effects["obstacles protection"][0]):
				frictions.append(PLAYER_FRICTION[obj.type][obj.subtype])
			
			else:
				frictions.append(PLAYER_FRICTION["normal"])

		if all([True if x == "normal" else False for x in frictions]) or not hits:
			total = PLAYER_FRICTION["normal"]
		
		else:	
			total = sum(set(frictions))

		return total


	def item_collide(self):
		hits = pg.sprite.spritecollide(self, ent.ITEMS, False)
		for item in hits:

			if item.subtype == "coin":
				self.coin_count += item.value
				item.collect()
			
			elif item.subtype == "rune":
				self.effects[item.effect][0] = True
				self.effects[item.effect][1] = EFFECTS_LONG[item.effect]

				if not item.effect in self.effect_order:
					self.effect_order.append(item.effect)
					UI.Effect(len(self.effect_order)-1, item.effect)
				
				item.collect()


	def harmful_collide(self):
		if self.counter["hurt freq"][0] and not self.effects["protection"][0]:
			
			self.rect = self.rect.inflate(3, 3)
			hits = pg.sprite.spritecollide(self, ent.PLAYER_HARMFUL, False)
			self.rect = self.rect.inflate(-3, -3)
			
			if hits:
				if not self.animation_control["death"]["normal"][0]:
					stn.change_animation(self, "idle", "injured")

				for k, v in PLAYER_DAMAGE.items():
					if any([True for x in hits if x.harm == k]): self.hurt(v)
			
			else:
				if self.animation_control["idle"]["injured"][0]:
					stn.change_animation(self, "idle", "normal")


	def special_collide(self):
		self.item_collide()

		hits = pg.sprite.spritecollide(self, ent.SPECIALS, False)
		for hit in hits:

			if hit.type == "portal":
				self.pos = pg.math.Vector2(hit.get_dist()) * TILE_SIZE

			elif hit.type == "trigger":
				hit.press()

			elif hit.type == "river":
				self.life = 0


	def die(self):
		for msg in self.ent_massages:
			msg.disapear = True
			msg.appear = False

		change_animation(self, "death", "normal")

		if stn.does_go_animation_end(self, "death", "normal"):
			self.kill()


		self.lock = True

		pos_x = rd.randint(self.rect.left, self.rect.right)
		pos_y = rd.randint(self.rect.top, self.rect.bottom)
		prt.Particle([pos_x, pos_y], [0, 0], rd.randint(4, 7), False, (200, 100, 106))


	def effect(self):
		if self.effects["curing"][0]:
			if self.counter["cure effe"][0]:
				if self.life < 20: self.heal(2)

		for pro in self.effects.values():
			if pro[0]:
				pro[1] -= 1
				if not pro[1]:
					pro[0] = False

	
	def shuting(self):
		dire = vec(0, 0)

		keys = pg.key.get_pressed()
		if keys[K_LEFT]:
			dire.x = -1
		if keys[K_RIGHT]:
			dire.x = 1
		if keys[K_UP]:
			dire.y = -1
		if keys[K_DOWN]:
			dire.y = 1

		if self.counter["shut freq"][1] >= 3:
			if keys[K_LEFT] or keys[K_RIGHT] or keys[K_UP] or keys[K_DOWN]:
				self.counter["shut freq"][1] = 0
				bl = sh.Bullet((self.pos.x, self.pos.y), ent.groups["bullet"], dire)
				stn.level.sprites(bl)


	def movement(self):
		self.acc = vec(0, 0)

		keys = pg.key.get_pressed()
		if keys[K_a]:
			self.acc.x = -PLAYER_ACC
		if keys[K_d]:
			self.acc.x = PLAYER_ACC
		if keys[K_w]:
			self.acc.y = -PLAYER_ACC
		if keys[K_s]:
			self.acc.y = PLAYER_ACC

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

			prt.Particle([pos_x, pos_y], [0, 0], rd.randint(2, 4), False, (200, 200, 200))

			
	def update(self):
		for name, count in self.counter.items():
			count[1] += 0.1
			if count[1]//1 == count[2]:
				count[1] = 0
				count[0] = True
			else:
				count[0] = False
		
		self.movement()
		if not self.lock:
			self.shuting()
		self.special_collide()
		self.harmful_collide()
		self.effect()
		animation_update(self)

		self.dest_radius = self.life * 2.5
		if self.dest_radius < self.radius:
			self.radius -= 1
		if self.dest_radius > self.radius:
			self.radius += 1

		if self.radius > 0: prt.Light((self.rect.center[0], self.rect.center[1]), self.radius, False, (50, 50, 70))

		if self.life <= 0:
			self.life = 0
			self.die()
	
		if self.life > self.max_life:
			self.life = self.max_life
