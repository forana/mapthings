import math
import random
import numpy
from scipy.spatial import Voronoi

ROOT3 = math.sqrt(3)

class Generator:
	""" Generates a number of sites based on a maximum width and height. """
	def generate(self, width, height):
		return []

	""" Returns the number of neighbors a tile has that would be considered "most". """
	def neighbor_threshold(self):
		return 1

def _relax(sites):
	diagram = Voronoi(sites)
	centers = []
	for region in diagram.regions:
		if len(region) > 0 and -1 not in region:
			centers.append(_centroid(map((lambda p: diagram.vertices[p]), region)))
	return centers

def _centroid(vertices):
	xm = numpy.mean(list(v[0] for v in vertices))
	ym = numpy.mean(list(v[1] for v in vertices))
	return (xm,ym)

class Arbitrary(Generator):
	def __init__(self, count, relaxations):
		self.count = count
		self.relaxations = relaxations

	def generate(self, width, height):
		sites = []
		for i in range(self.count):
			site = (random.randint(0, width), random.randint(0, height))
			sites.append(site)
		for i in range(self.relaxations):
			sites = _relax(sites)
		return sites

	def neighbor_threshold(self):
		return 4

class Square(Generator):
	def __init__(self, side):
		self.side = side

	def generate(self, width, height):
		sites = []
		half = self.side / 2
		for y in range(-2 * self.side, height + self.side * 2, self.side):
			for x in range(-2 * self.side, width + self.side * 2, self.side):
				sites.append((x + half, y + half))
		return sites

	def neighbor_threshold(self):
		return 3

class Triangle(Generator):
	def __init__(self, side):
		self.side = side

	def generate(self, width, height):
		sites = []
		halfbase = self.side / 2
		triheight = halfbase * ROOT3
		centeroffset = halfbase / ROOT3
		for y in range(-2, int(math.ceil(height / triheight)) + 2):
			for x in range(-2, int(math.ceil(width / halfbase)) + 2):
				xp = x * halfbase
				yp = y * triheight
				if (x + y) % 2 == 0 : # base-down
					yp += triheight - centeroffset
				else:
					yp += centeroffset
				sites.append((xp, yp))
		return sites

	def neighbor_threshold(self):
		return 2

class Hexagon(Generator):
	def __init__(self, side):
		self.side = side

	def generate(self, width, height):
		sites = []
		horizontal_spacing = self.side * 3
		vertical_spacing = self.side * ROOT3
		horizontal_offset = self.side * 3 / 2
		vertical_offset = vertical_spacing / 2
		for y in range(-2, int(math.ceil(height / vertical_offset)) + 2):
			for x in range(-2, int(math.ceil(height / horizontal_offset)) + 2):
				xp = x * horizontal_spacing
				yp = y * vertical_offset
				if y % 2 == 1:
					xp += horizontal_offset
				sites.append((xp, yp))
		return sites

	def neighbor_threshold(self):
		return 4
