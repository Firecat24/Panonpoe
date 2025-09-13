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

from .routes.routes_submit import bp_submit
from .routes.routes_dashboard import bp_dashboard
app.register_blueprint(bp_dashboard)
app.register_blueprint(bp_submit)