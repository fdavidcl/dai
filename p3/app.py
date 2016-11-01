#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, escape, render_template, request, redirect, url_for, session
from collections import deque

app = Flask(__name__)

@app.after_request
def save_history(response):
    if "username" in session and request.method == "GET" and response.mimetype == "text/html":
        try:
            h = deque(session["history"], 3)
            h.append(request.path)
            session["history"] = list(h)
            session.modified = True
        except:
            session["history"] = [request.path]
    return response

@app.route("/")
def index():
    if "username" in session:
        return render_template("index_logged.html", username=session["username"])
    else:
        return render_template("index.html")

@app.route("/users/login/", methods=['POST'])
def login():
    session.clear()
    return redirect(url_for("index"))

@app.route("/users/logout/")
def logout():
    session.pop("username", None)
    session.pop("history", None)
    return redirect(url_for("index"))

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/datasets/")
def datasets():
    return render_template("datasets.html") if "username" in session else abort(404)

@app.route("/models/")
def models():
    return render_template("models.html") if "username" in session else abort(404)
    

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

# set the secret key.  keep this really secret:
app.secret_key = '=U][Eb\\v^`4gh9wd@:L;?WAa2SiMmBx<'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
