from flask import Blueprint, render_template, request, redirect, url_for, flash

bp_produk = Blueprint("main_produk", __name__)

@bp_produk.route("/drone", endpoint="drone")
def drone():
    return render_template("drone.html")

@bp_produk.route("/watch", endpoint="watch")
def watch():
    return render_template("watch.html")

@bp_produk.route("/livecam", endpoint="livecam")
def livecam():
    return render_template("livecam.html")

@bp_produk.route("/hoverboard", endpoint="hoverboard")
def hoverboard():
    return render_template("hoverboard.html")

@bp_produk.route("/bike", endpoint="bike")
def bike():
    return render_template("bike.html")

@bp_produk.route("/headphone", endpoint="headphone")
def headphone():
    return render_template("headphone.html")

@bp_produk.route("/proapp", endpoint="proapp")
def proapp():
    return render_template("proapp.html")