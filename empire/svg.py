import simplesvg
import random
import gamemap

def map_to_svg(m):
	svg = simplesvg.SVG(m.width, m.height)
	land = simplesvg.rgb(0x99, 0xFF, 0xCC)
	ocean = simplesvg.rgb(0x66, 0x99, 0xCC)
	unknown = "yellow"
	for tile in m.tiles:
		fill = land if tile.terrain == gamemap.LAND else ocean if tile.terrain == gamemap.OCEAN else unknown
		svg.polygon(tile.vertices, fill = fill, stroke = fill, strokeWidth = 1, id = tile.id, neighbors = ",".join(list(neighbor.id for neighbor in tile.neighbors)))
	return svg.to_xml()
