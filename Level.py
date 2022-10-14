from objects import player, walls, special, items, obstacles, entities

import pygame as pg
import Object as obj
import Settings as stn
import os
import json

class Level:
	def __init__(self, name):
		self.objects = {}
		self.level = {}
		self.sprites_prop = {}
		self.folder = os.path.join(os.path.dirname(__file__), "levels")

		stn.images_folder = os.path.join(os.path.dirname(__file__), "src")
		stn.level = self

		with open(os.path.join(self.folder, f"{name}.json")) as f:
			self.level = json.load(f)
			stn.metadata = self.level["metadata"]

		with open(os.path.join(stn.images_folder, "sprites.json")) as f:
			self.sprites_prop = json.load(f)

	def clear_level(sels): # kill all the sprites so theres no objects on the level
		for obj in obj.SPRITES:
			obj.kill()
		for prt in obj.PARTICLES:
			prt.kill()

	def load_object(self, object): # load the object to the virtual map
		
		if object.type in self.objects:
			self.objects[object.type][object.loc] = object
		else:
			self.objects[object.type] = {}
			self.objects[object.type][object.loc] = object

	def decipher_level(self): # just generate the lecvel by the json file, at the same time make virtual map
		for loc, tile in self.level.items():
			if loc == "metadata": continue
			loc = tuple(map(int, loc.split(" ")))

			if tile["type"] == "item":
				if tile["subtype"] == "coin":
					items.Coin(loc, obj.groups["coin"], tile["value"])
				elif tile["subtype"] == "rune":
					items.Rune(loc, obj.groups["rune"], tile["effect"])

			elif tile["type"] == "wall":
				if tile["subtype"] == "frozen":
					walls.Frozen(loc, obj.groups["frozen"])
				elif tile["subtype"] == "sandy":
					walls.Sandy(loc, obj.groups["sandy"])
				elif tile["subtype"] == "harmful":
					walls.Harmful(loc, obj.groups["harmful"])
				elif tile["subtype"] == "glow":
					walls.Glow(loc, obj.groups["glow"])

			elif tile["type"] == "obstacles":
				if tile["subtype"] == "jeli":
					obstacles.Jeli(loc, obj.groups["jeli"])
				elif tile["subtype"] == "tar":
					obstacles.Tar(loc, obj.groups["tar"])
				elif tile["subtype"] == "poisoned":
					obstacles.Poisoned(loc, obj.groups["poisoned"])

			elif tile["type"] == "special":
				if tile["subtype"] == "portal":
					special.Portal(loc, obj.groups["portal"], tile["dist"])
				elif tile["subtype"] == "river":
					self.load_object(special.River(loc, obj.groups["river"]))
				elif tile["subtype"] == "trigger":
					special.Trigger(loc, obj.groups["trigger"])

			elif tile["type"] == "entity":
				if tile["subtype"] == "enemy":
					entities.Enemy(loc, obj.groups["enemy"])

			elif tile["type"] == "player":
				obj.PLAYER = player.Player(loc, obj.groups["player"])
	
	def sprites(self, specific=False): # sets the animation/images to the given sprites

		if not specific:

			for type in self.sprites_prop:
				if self.sprites_prop[type]["do animation"]:
					for ent in obj.unic_groups[type]:
						stn.set_animation(ent, self.sprites_prop[type]["animation prop"])

				else:
					for ent in obj.unic_groups[type]:
						stn.set_image(ent, pg.image.load(os.path.join(stn.images_folder, *self.sprites_prop[type]["image"])).convert_alpha())
		
		else:
			if hasattr(specific, "subtype"):
				stn.set_animation(specific, self.sprites_prop[specific.subtype]["animation prop"])
			else:
				stn.set_animation(specific, self.sprites_prop[specific.type]["animation prop"])

	def connect_objects(self): # call functions to sprites for connecting them with nearest sprites
		for type, loc in self.objects.items():
			for loc, object in loc.items():

				final = {"up":False, "down":False, "left":False, "right":False, "middle":False}

				new_loc = (loc[0], loc[1] - 1) # up

				if new_loc in self.objects[type].keys():
					final["up"] = True

				new_loc = (loc[0], loc[1] + 1) #down

				if new_loc in self.objects[type].keys():
					final["down"] = True

				new_loc = (loc[0] + 1, loc[1]) # right

				if new_loc in self.objects[type].keys():
					final["right"] = True

				new_loc = (loc[0] - 1, loc[1]) # left

				if new_loc in self.objects[type].keys():
					final["left"] = True

				if all(not x for x in final.values()):
					final["middle"] = True

				object.set_dire(final)


if __name__ == '__main__': # only for dev
	import Main as m
	main = m.Main()
	main.main_loop()