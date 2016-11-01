#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, escape, render_template, request, redirect, url_for
import codecs
import mandelbrot
import random_svg

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", code=escape(codecs.open("practica2.py", "r", "utf-8").read()))

@app.route("/user/")
def login():
    if request.args.get("login", ""):
        return redirect(url_for("user", username=request.args.get("login", "")))
    return render_template("login.html")

@app.route("/user/<username>/")
def user(username):
    return render_template("user.html", username=username)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

@app.route("/mandelbrot/")
def mndlbrt():
    args = {
        "width": 500,
        "x1": -2.5,
        "y1": 1.0,
        "x2": 1,
        "y2": -1
    }

    for arg in args.keys():
        if request.args.get(arg, ""):
            args[arg] = float(request.args.get(arg, ""))
    
    return render_template("mandelbrot.html",
                           image=mandelbrot.mandelbrot_base64(int(args["width"]), (args["x1"], args["y1"]), (args["x2"], args["y2"])),
                           code=escape(codecs.open("mandelbrot.py", "r", "utf-8").read()))

@app.route("/svg/")
def svg():
    return render_template("random_svg.html", image=random_svg.random_svg(), code=escape(codecs.open("random_svg.py", "r", "utf-8").read()))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
