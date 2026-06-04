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
    extra_domes = [
        {
            # Walaupun cuma 1 gambar, tetap bungkus dalam list [ ]
            "images": [
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_ta.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_ta1.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_ta2.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_ta3.jpeg"
            ],
            "name": "Diameter = 7.5 cm - type A",
            "url": "https://tk.tokopedia.com/ZSDVPb6me/"
        },
        {
            "images": [
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_tb.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_tb1.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_tb2.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_tb3.jpeg"
            ],
            "name": "Diameter = 7.5 cm - type B",
            "url": "https://tk.tokopedia.com/ZSDVPs7Wg/"
        },
        {
            "images": [
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_tc.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_tc1.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_tc2.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7.5cm_tc3.jpeg"
            ],
            "name": "Diameter = 7.5 cm - type C",
            "url": "https://tk.tokopedia.com/ZSDVPoYWy/"
        },
        {
            "images": [
                "assets/img/headphone/dome_akrilik_ekstra/7cm.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7cm1.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7cm2.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/7cm3.jpeg"
            ],
            "name": "Diameter = 7 cm",
            "url": "https://tk.tokopedia.com/ZSDVPCvfk/"
        },
        {
            "images": [
                "assets/img/headphone/dome_akrilik_ekstra/8cm_ta.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/8cm_ta1.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/8cm_ta2.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/8cm_ta3.jpeg"
            ],
            "name": "Diameter = 8 cm - type A",
            "url": "https://tk.tokopedia.com/ZSDV56Mqh/"
        },
        {
            "images": [
                "assets/img/headphone/dome_akrilik_ekstra/8cm_tb.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/8cm_tb1.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/8cm_tb2.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/8cm_tb3.jpeg"
            ],
            "name": "Diameter = 8 cm - type B",
            "url": "https://tk.tokopedia.com/ZSDV5fv5k/"
        },
        {
            "images": [
                "assets/img/headphone/dome_akrilik_ekstra/9cm_ta.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/9cm_ta1.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/9cm_ta2.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/9cm_ta3.jpeg"
            ],
            "name": "Diameter = 9 cm - type A",
            "url": "https://tk.tokopedia.com/ZSDVPEgCq/"
        },
        {
            "images": [
                "assets/img/headphone/dome_akrilik_ekstra/9cm_tb.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/9cm_tb1.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/9cm_tb2.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/9cm_tb3.jpeg"
            ],
            "name": "Diameter = 9 cm - type B",
            "url": "https://tk.tokopedia.com/ZSDVPEgCq/"
        },
        {
            "images": [
                "assets/img/headphone/dome_akrilik_ekstra/18cm.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/18cm1.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/18cm2.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/18cm3.jpeg",
                "assets/img/headphone/dome_akrilik_ekstra/18cm4.jpeg"
            ],
            "name": "Diameter = 18 cm",
            "url": "https://tk.tokopedia.com/ZSDVPEgCq/"
        }
    ]
    return render_template("akrilikdome.html", domes=domes, extra_domes=extra_domes)