from flask import Blueprint, render_template, request, redirect, url_for, flash

bp_teleskop = Blueprint("main_teleskop", __name__)

@bp_teleskop.route("/", methods=["GET"])
def teleskop():
    return render_template("teleskop.html")