import generator
import landfill
from scipy.spatial import Voronoi

UNKNOWN = -1
OCEAN = 1
LAND = 2

class Map:
	def __init__(self, sites, width, height, fill_strategy, neighbor_threshold):
		self.tiles = []
		self.width = width
		self.height = height
		diagram = Voronoi(sites)
		for tile in self.__build_tiles(diagram):
			self.tiles.append(tile)
		self.__evaluate_borders();
		fill_strategy(self, neighbor_threshold)

	def __build_tiles(self, diagram):
		tiles = {}
		for i in range(len(diagram.points)):
			id = i
			vertices = []
			point = diagram.points[i]
			region = diagram.regions[diagram.point_region[i]]
			if -1 not in region: # -1 means "not in diagram" - it can happen
				for vi in region:
					raw_vertex = diagram.vertices[vi]
					int_vertex = (int(raw_vertex[0]), int(raw_vertex[1]))
					vertices.append(int_vertex)
				tile = Tile(id, point, vertices)
				tiles[id] = tile
		return self.__pair_neighbors(tiles, diagram)

	def __pair_neighbors(self, tiles, diagram):
		point_neighbors = {}
		for ridge in diagram.ridge_points:
			# need to check this to make sure one didn't get filtered out
			if ridge[0] in tiles and ridge[1] in tiles:
				# ridges aren't guaranteed to not be mirrored - need to check
				tile1 = tiles[ridge[0]]
				tile2 = tiles[ridge[1]]
				if tile2 not in tile1.neighbors:
					tile1.neighbors.append(tile2)
					tile2.neighbors.append(tile1)
		return tiles.values()

	def __evaluate_borders(self):
		for tile in self.tiles:
			tile.border = False
			for vertex in tile.vertices:
				if vertex[0] <= 0 or vertex[0] >= self.width or vertex[1] <= 0 or vertex[1] >= self.height:
					tile.border = True
					break

	def tile_at(self, point):
		mindist = None
		mintile = None
		for tile in self.tiles:
			dist = tile.distance_to(point)
			if mindist is None or dist < mindist:
				mindist = dist
				mintile = tile
		return mintile

class Tile:
	def __init__(self, id, center, vertices):
		self.id = str(id)
		self.center = center
		self.vertices = vertices
		self.neighbors = []
		self.terrain = UNKNOWN
		self.elevation = float("inf")
		self.border = False

	def distance_to(self, point):
		from math import hypot
		return hypot(self.center[0] - point[0], self.center[1] - point[1])

	def __repr__(self):
		return "Tile #%s @ (%d, %d)" % (self.id, self.center[0], self.center[1])

def generate(width, height, site_generator = generator.Arbitrary(count = 1000, relaxations = 2), fill_strategy = landfill.fill_radial):
	return Map(site_generator.generate(width, height), width, height, fill_strategy, site_generator.neighbor_threshold())
