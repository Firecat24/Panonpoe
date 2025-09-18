from flask import Blueprint, render_template, request, redirect, url_for, flash

bp_dashboard = Blueprint("main_dashboard", __name__)

@bp_dashboard.route("/", methods=["GET"])
def index():
    return render_template("index.html")