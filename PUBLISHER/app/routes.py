from flask import Blueprint, jsonify, g, render_template

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return "Hello from Flask!"
