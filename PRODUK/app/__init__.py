from flask import Flask, g
from .db.db import Database

app = Flask(__name__)

# @app.before_request
# def before_request():
#     g.db = Database()
#     g.db.connect()

# @app.teardown_request
# def teardown_request(exception):
#     if hasattr(g, "db"):
#         g.db.disconnect()

from .routes.routes_dashboard import bp_dashboard
from .routes.routes_akrilikdome import bp_akrilikdome
from .routes.routes_siqilat import bp_siqiblat
from .routes.routes_teleskop import bp_teleskop
app.register_blueprint(bp_dashboard)
app.register_blueprint(bp_akrilikdome, url_prefix="/akrilikdome")
app.register_blueprint(bp_siqiblat, url_prefix="/siqilat")
app.register_blueprint(bp_teleskop, url_prefix="/teleskop")