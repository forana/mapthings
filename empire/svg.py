import simplesvg
import random
import map

def map_to_svg(m):
	svg = simplesvg.SVG(m.width, m.height)
	land = simplesvg.rgb(0x99, 0xFF, 0xCC)
	ocean = simplesvg.rgb(0x66, 0x99, 0xCC)
	for tile in m.tiles:
		fill = land if tile.terrain == map.LAND else ocean
		svg.polygon(tile.vertices, fill = fill, stroke = "white", strokeWidth = 1, desc = repr(tile))
	return svg.to_xml()
