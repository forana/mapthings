import gamemap
import random
from util import IndexedList

def fill_radial(m):
	radius = min(m.width, m.height) / 2 * 0.9
	point = (m.width / 2, m.height / 2)
	for tile in m.tiles:
		if tile.distance_to(point) < radius and not tile.border:
			tile.terrain = gamemap.LAND
			tile.elevation = 1
		else:
			tile.terrain = gamemap.OCEAN
			tile.elevation = 0

def fill_random(m):
	threshhold = 0.3
	for tile in m.tiles:
		if tile.border or random.random() < threshhold:
			tile.terrain = gamemap.OCEAN
			tile.elevation = 0
		else:
			tile.terrain = gamemap.LAND
			tile.elevation = 1

def fill_spread(m):
	queue = IndexedList()
	ocean_tiles = IndexedList()
	# 1) find borders, add them to queue and assign them as ocean
	for tile in m.tiles:
		if tile.border:
			queue.append(tile)
			tile.terrain = gamemap.OCEAN
			ocean_tiles.append(tile)
	# 2) start our index
	index = len(queue) # the index of the one we're about to add
	# 3) start with the center tile
	tile = m.tile_at((m.width / 2, m.height / 2))
	queue.append(tile)
	base_land_chance = 0.6
	chance_modifier = 0.1
	land_count = 1
	minimum_land = len(m.tiles) / 10
	# 4) spread out
	while index < len(queue):
		tile = queue[index]
		land_chance = base_land_chance
		for neighbor in tile.neighbors:
			if neighbor.terrain == gamemap.LAND:
				land_chance += chance_modifier
			elif neighbor.terrain == gamemap.OCEAN:
				land_chance -= chance_modifier
			if neighbor not in queue:
				queue.append(neighbor)
		if random.random() <= land_chance or land_count < minimum_land:
			tile.terrain = gamemap.LAND
			land_count += 1
		else:
			tile.terrain = gamemap.OCEAN
			ocean_tiles.append(tile)
		index += 1
	# 5) assign elevations as distance from water... sort of
	queue = ocean_tiles #cheating
	index = 0
	while index < len(queue):
		tile = queue[index]
		if tile.terrain == gamemap.OCEAN:
			tile.elevation = 0
		else:
			tile.elevation = min(list(neighbor.elevation for neighbor in tile.neighbors)) + 1
		for neighbor in tile.neighbors:
			if neighbor not in queue:
				queue.append(neighbor)
		index += 1