from flask import Blueprint, render_template, request, redirect, url_for, flash

bp_akrilikdome = Blueprint("main_akrilikdome", __name__)

@bp_akrilikdome.route("/", methods=["GET"])
def akrilikdome():
    domes = [
        {
            "img": "../static/assets/img/headphone/dome_akrilik/d42.jpg",
            "name": "Diameter = 42 cm",
            "url": "https://tk.tokopedia.com/ZSDVPoYWy/"
        },
        {
            "img": "../static/assets/img/headphone/dome_akrilik/d60.jpg",
            "name": "Diameter = 60 cm",
            "url": "https://tk.tokopedia.com/ZSDVPb6me/"
        },
        {
            "img": "../static/assets/img/headphone/dome_akrilik/orange-d43.jpg",
            "name": "Diameter = 43 cm",
            "url": "https://tk.tokopedia.com/ZSDVPs7Wg/"
        },
        {
            "img": "../static/assets/img/headphone/dome_akrilik/replacement_cctv_outdoor.jpg",
            "name": "Diameter = 14.6 cm",
            "url": "https://tk.tokopedia.com/ZSDVPCvfk/"
        },
        {
            "img": "../static/assets/img/headphone/dome_akrilik/tipe-A.jpg",
            "name": "Diameter = 11 cm (type A)",
            "url": "https://tk.tokopedia.com/ZSDV56Mqh/"
        },
        {
            "img": "../static/assets/img/headphone/dome_akrilik/tipe-B.jpg",
            "name": "Diameter = 11 cm (type B)",
            "url": "https://tk.tokopedia.com/ZSDV5fv5k/"
        },
        {
            "img": "../static/assets/img/headphone/dome_akrilik/tipe-C.jpg",
            "name": "Diameter = 11 cm (type C)",
            "url": "https://tk.tokopedia.com/ZSDVPEgCq/"
        },
    ]
    return render_template("akrilikdome.html", domes=domes)