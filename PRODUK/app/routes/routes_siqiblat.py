from flask import Blueprint, render_template, request, redirect, url_for, flash

bp_siqiblat = Blueprint("main_siqiblat", __name__)

@bp_siqiblat.route("/", methods=["GET"])
def siqiblat():
    return render_template("siqiblat.html")