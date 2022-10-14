import pygame as pg
from pygame.locals import *
from Settings import *

PARTICLES = pg.sprite.Group()
SPRITES = pg.sprite.Group()
UI = pg.sprite.Group()

PLAYER_COLLIDED = pg.sprite.Group()
ENTITY_COLLIDED = pg.sprite.Group()
PLAYER_HARMFUL = pg.sprite.Group()
ENTITY_HARMFUL = pg.sprite.Group()
PLAYER_FRIC_INFLUES = pg.sprite.Group()

ENTITY_MESSAGES = pg.sprite.Group()
LIFE_BAR = pg.sprite.Group()
HEARTS = pg.sprite.Group()
EFFECTS = pg.sprite.Group()
HOVER_MESSAGE = pg.sprite.Group()

PLAYER_GS = pg.sprite.GroupSingle()
WALLS = pg.sprite.Group()
ITEMS = pg.sprite.Group()
SPECIALS = pg.sprite.Group()
OBSTRACLES = pg.sprite.Group()
SHOOTING = pg.sprite.Group()
ENTITY = pg.sprite.Group()

FROZEN = pg.sprite.Group()
SANDY = pg.sprite.Group()
HARMFUL = pg.sprite.Group()
GLOW = pg.sprite.Group()

COIN = pg.sprite.Group()
RUNE = pg.sprite.Group()

PORTAL = pg.sprite.Group()
RIVER = pg.sprite.Group()
TRIGGER = pg.sprite.Group()

BULLET = pg.sprite.Group()
JELI = pg.sprite.Group()
TAR = pg.sprite.Group()
POISONED = pg.sprite.Group()

ENEMY = pg.sprite.Group()
PLAYER = PLAYER_GS.sprites()

LIGHT = pg.sprite.Group()
PARTICLE = pg.sprite.Group()
LIGHT_PARTICKLES = pg.sprite.Group()

light_particles = []
level = None

groups = {
	"coin": [SPRITES, ITEMS, COIN],
	"rune": [SPRITES, ITEMS, RUNE],
	"frozen": [SPRITES, WALLS, FROZEN, PLAYER_COLLIDED, PLAYER_FRIC_INFLUES, ENTITY_COLLIDED],
	"sandy": [SPRITES, WALLS, SANDY, PLAYER_COLLIDED, PLAYER_FRIC_INFLUES, ENTITY_COLLIDED],
	"harmful": [SPRITES, WALLS, HARMFUL, PLAYER_COLLIDED, ENTITY_COLLIDED, PLAYER_HARMFUL, ENTITY_HARMFUL],
	"glow": [SPRITES, WALLS, GLOW, PLAYER_COLLIDED, ENTITY_COLLIDED],
	"jeli": [SPRITES, OBSTRACLES, JELI, PLAYER_FRIC_INFLUES],
	"tar": [SPRITES, OBSTRACLES, TAR, PLAYER_FRIC_INFLUES],
	"poisoned": [SPRITES, OBSTRACLES, POISONED, PLAYER_FRIC_INFLUES, PLAYER_HARMFUL],
	"portal": [SPRITES, SPECIALS, PORTAL],
	"river": [SPRITES, SPECIALS, RIVER, PLAYER_COLLIDED, ENTITY_COLLIDED],
	"trigger": [SPRITES, SPECIALS, TRIGGER],
	"bullet": [SPRITES, SHOOTING, BULLET],
	"enemy": [SPRITES, ENTITY, ENEMY, PLAYER_COLLIDED, ENTITY_COLLIDED, PLAYER_HARMFUL],
	"player": [SPRITES, PLAYER_GS, ENTITY, ENTITY_COLLIDED]
}

unic_groups = {
	"collide": PLAYER_COLLIDED,
	"fric influes": PLAYER_FRIC_INFLUES,
	"special": SPECIALS,
	"items": ITEMS,
	"coin": COIN,
	"rune": RUNE,
	"walls": WALLS,
	"frozen": FROZEN,
	"sandy": SANDY,
	"harmful": HARMFUL,
	"glow": GLOW,
	"obstacles": OBSTRACLES,
	"jeli": JELI,
	"tar": TAR,
	"poisoned": POISONED,
	"specials": SPECIALS,
	"portal": PORTAL,
	"river": RIVER,
	"trigger": TRIGGER,
	"bullet": BULLET,
	"enemy": ENEMY,
	"player": PLAYER_GS
}


if __name__ == '__main__': # only for dev
	import Main as m
	main = m.Main()
	main.main_loop()