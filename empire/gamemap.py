import generator
import landfill
from scipy.spatial import Voronoi

UNKNOWN = -1
OCEAN = 1
LAND = 2

class Map:
	def __init__(self, sites, width, height, fill_strategy = landfill.fill_radial):
		self.tiles = []
		self.width = width
		self.height = height
		diagram = Voronoi(sites)
		for tile in self.__build_tiles(diagram):
			self.tiles.append(tile)
		self.__evaluate_borders();
		fill_strategy(self)

	def __build_tiles(self, diagram):
		tiles = []
		for i in range(len(diagram.points)):
			id = i
			vertices = []
			point = diagram.points[i]
			region = diagram.regions[diagram.point_region[i]]
			if -1 not in region:
				for vi in region:
					vertices.append(diagram.vertices[vi])
				tile = Tile(id, point, vertices)
				tiles.append(tile)
		return tiles

	def __evaluate_borders(self):
		for tile in self.tiles:
			tile.border = False
			for vertex in tile.vertices:
				if vertex[0] <= 0 or vertex[0] >= self.width or vertex[1] <= 0 or vertex[1] >= self.height:
					tile.border = True
					break

	def get_tile_for_point(self, point):
		mindist = None
		mintile = None
		for id, tile in self.tiles:
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

def generate(width, height, site_generator = generator.Arbitrary(count = 1000, relaxations = 2)):
	return Map(site_generator.generate(width, height), width, height)
