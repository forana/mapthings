import flask
import sqlalchemy

import empire.config

empire.config.load_properties("game.conf")

engine = sqlalchemy.create_engine(empire.config.get_property("DB_URL"), echo = False )

app = flask.Flask(__name__)

@app.route("/")
def root():
	return "haha world"

if __name__ == "__main__":
	app.run(port = int(empire.config.get_property("WEB_PORT")))
