import flask
import sqlalchemy
import os

import empire.config

import empire.gamemap
import empire.svg
import empire.generator
import empire.landfill

empire.config.load_properties("game.conf")

engine = sqlalchemy.create_engine(empire.config.get_property("DB_URL"), echo = False )

app = flask.Flask(__name__)

@app.route("/")
def root():
	return "good"

@app.route("/map", defaults={"opt": "arbitrary"})
@app.route("/map/<string:opt>")
def maptest(opt):
	width = int(flask.request.args.get("width", "600"))
	height = int(flask.request.args.get("height", "600"))
	generator = None
	if opt == "square":
		generator = empire.generator.Square(20)
	elif opt == "triangle":
		generator = empire.generator.Triangle(20)
	elif opt == "hexagon":
		generator = empire.generator.Hexagon(15)
	else: # default is "arbitrary"
		generator = empire.generator.Arbitrary(1000, 3)
	fill_strategy = empire.landfill.fill_spread
	m = empire.gamemap.generate(width, height, site_generator = generator, fill_strategy = fill_strategy)
	return flask.Response(empire.svg.map_to_svg(m), mimetype = "image/svg+xml")

port = int(os.getenv("PORT", empire.config.get_property("WEB_PORT")))
print "SHIT MAN", port
app.run(host = "0.0.0.0", port = port)
