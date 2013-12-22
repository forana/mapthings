import simplesvg
import random
import gamemap
import numpy

def __rgb_merge(c1, c2, n):
	cr = [c1[0], c1[1], c1[2]]
	for i in range(n):
		for c in range(3):
			cr[c] = numpy.mean([cr[c], c2[c]])
	return simplesvg.rgb(cr[0], cr[1], cr[2])

def map_to_svg(m):
	svg = simplesvg.SVG(m.width, m.height)
	land = (0x99, 0xFF, 0xCC)
	mountain = (0x80, 0x65, 0x19)
	ocean = simplesvg.rgb(0x66, 0x99, 0xCC)
	unknown = "yellow"
	for tile in m.tiles:
		fill = __rgb_merge(land, mountain, tile.elevation - 1) if tile.terrain == gamemap.LAND else ocean if tile.terrain == gamemap.OCEAN else unknown
		svg.polygon(tile.vertices, fill = fill, stroke = fill, strokeWidth = 1, id = tile.id, neighbors = ",".join(list(neighbor.id for neighbor in tile.neighbors)))
	return svg.to_xml()
