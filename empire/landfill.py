import map

def fill_radial(m):
	radius = min(m.width, m.height) / 2 * 0.9
	point = (m.width / 2, m.height / 2)
	for tile in m.tiles:
		if tile.distance_to(point) < radius:
			tile.terrain = map.LAND
		else:
			tile.terrain = map.OCEAN
