from flask import Blueprint, render_template, request, redirect, url_for, flash

bp_akrilikdome = Blueprint("main_akrilikdome", __name__)

@bp_akrilikdome.route("/", methods=["GET"])
def akrilikdome():
    return render_template("akrilikdome.html")