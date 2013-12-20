import gamemap

def fill_radial(m):
	radius = min(m.width, m.height) / 2 * 0.9
	point = (m.width / 2, m.height / 2)
	for tile in m.tiles:
		if tile.distance_to(point) < radius:
			tile.terrain = gamemap.LAND
		else:
			tile.terrain = gamemap.OCEAN
