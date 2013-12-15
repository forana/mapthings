import flask
import sqlalchemy

import empire.config

empire.config.load_properties("game.conf")

engine = sqlalchemy.create_engine(empire.config.get_property("DB_URL"), echo = False )

app = flask.Flask(__name__)
app.debug = True

@app.route("/")
def root():
	return "haha world"

# map generation using perlin noise
@app.route("/maptest")
def maptest():
	import noise
	s = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1000px" height="1000px">'
	octaves = 1
	freq = 16
	for y in range(0, 1000, 10):
		line = []
		for x in range(0, 1000, 10):
			i = int(noise.snoise2(x / freq, y / freq, octaves) * 256)
			s += '<rect x="{x}px" y="{y}px" width="10" height="10" style="fill:rgb({i},{i},{i})"/>'.format(x=str(x), y=str(y), i=str(i))
	return flask.Response(s + "</svg>", mimetype = "image/svg+xml")

# map generation using voronoi diagram
@app.route("/maptest2")
def maptest2():
	from scipy.spatial import Voronoi
	import numpy
	import random
	from Queue import Queue
	points = []
	width = 500
	height = 500
	for dc in range(1000):
		points.append([random.randint(0, width), random.randint(0, height)])
	def centroid(a):
		xs = 0
		ys = 0
		for p in a:
			xs += p[0]
			ys += p[1]
		return [xs/len(a), ys/len(a)]
	def lloydrelax(a):
		diagram = Voronoi(a)
		r = []
		for region in diagram.regions:
			if len(region) > 0 and -1 not in region:
				r.append(centroid(map((lambda p: diagram.vertices[p]), region)))
		return r
	relaxations = 2
	for r in range(relaxations):
		points = lloydrelax(points)
	diagram = Voronoi(points)
	s = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="500px" height="500px">'
	def pair(a):
		return str(a[0])+","+str(a[1])
	ridges = ""
	borders = []
	point_neighbors = {}
	for ridge in diagram.ridge_points:
		if -1 not in ridge:
			x1 = diagram.points[ridge[0]][0]
			y1 = diagram.points[ridge[0]][1]
			x2 = diagram.points[ridge[1]][0]
			y2 = diagram.points[ridge[1]][1]
			ridges += '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="blue" stroke-width="1"/>'.format(x1 = x1, y1 = y1, x2 = x2, y2 = y2)
			if ridge[0] not in point_neighbors:
				point_neighbors[ridge[0]] = [ridge[1]]
			else:
				point_neighbors[ridge[0]].append(ridge[1])
			if ridge[1] not in point_neighbors:
				point_neighbors[ridge[1]] = [ridge[0]]
			else:
				point_neighbors[ridge[1]].append(ridge[0])
	elevations = {}
	elqueue = Queue()
	for i in range(len(diagram.points)):
		region = diagram.regions[diagram.point_region[i]]
		border = -1 in region
		if not border:
			for vi in region:
				vertex = diagram.vertices[vi]
				if vertex[0] < 0 or vertex[0] > width or vertex[1] < 0 or vertex[1] > height:
					border = True
					break
		if border:
			print i
			for vi in region:
				print diagram.vertices[vi]
			elevations[i] = 0
			elqueue.put(i)
	while not elqueue.empty():
		i = elqueue.get()
		if i in elevations:
			for neighbor in point_neighbors[i]:
				if neighbor not in elevations:
					elqueue.put(neighbor)
		else:
			total = 0
			for neighbor in point_neighbors[i]:
				if neighbor in elevations:
					total += elevations[neighbor]
				else:
					elqueue.put(neighbor)
			elevations[i] = total / len(point_neighbors[i]) + random.random()
	mean = numpy.mean(elevations.values())
	std = numpy.std(elevations.values())
	highest = max(elevations.values())
	sealevel = mean - std
	def make_brown(elevation):
		r = 0x85
		g = 0x60
		b = 0x17
		factor = 1 - (elevation - sealevel) / (highest - sealevel)
		return "rgb(%d,%d,%d)" % (int(r*factor), int(g*factor), int(b*factor))
	for pi in range(len(diagram.points)):
		color = "rgb(31,69,252)" if elevations[pi] <= sealevel else make_brown(elevations[pi])
		region = diagram.regions[diagram.point_region[pi]]
		if len(region) > 0 and -1 not in region:
			p = ('<path id="region-{id}" stroke="{color}" stroke-width="1" fill="{color}" d="M ' + pair(diagram.vertices[region[0]])).format(color = color, id = i)
			for i in region[1:]:
				if i>=0:
					p += " L " + pair(diagram.vertices[i])
			p += ' Z"/>'
			s += p
	"""for point in diagram.points:
		s += '<circle cx="{x}" cy="{y}" r="3" stroke-width="0" fill="black"/>'.format(x=point[0], y=point[1])
	"""
	s += "</svg>"
	return flask.Response(s, mimetype = "image/svg+xml")

if __name__ == "__main__":
	app.run(port = int(empire.config.get_property("WEB_PORT")))
