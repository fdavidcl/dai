#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, escape, render_template, request, redirect, url_for, session, abort
from collections import deque
import flask_shelve as shelve
import re

app = Flask(__name__)
app.config['SHELVE_FILENAME'] = 'shelve.db'
shelve.init_app(app)

@app.after_request
def save_history(response):
    if "username" in session and request.method == "GET" and response.mimetype == "text/html":
        try:
            h = deque(session["history"], 3)
            h.appendleft(request.path)
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

@app.route("/users/login/", methods=["POST"])
def login():
    username = request.form["username"]
    key = "users:{}".format(username)
    db = shelve.get_shelve('r')
    if key in db and db[key]["password"] == request.form["password"]:
        session["username"] = request.form["username"]
        session["history"] = []
        
    return redirect(url_for("index"))
    
@app.route("/users/logout/")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/users/signup/")
def signup():
    return render_template("signup.html")

@app.route("/users/", methods=["POST"])
def new_user():
    username = request.form["username"]
    if re.match(r"^([a-zA-Z0-9]+)$", username):
        db = shelve.get_shelve('c')
        if "users:{}".format(username) not in db:
            db["users:{}".format(username)] = {
                "username": username,
                "password": request.form["password"], # aquí iría el hash de la contraseña
                "realname": request.form["realname"],
                "email":    request.form["email"]
            }
            return redirect(url_for("index"))
        else:
            return redirect(url_for("signup"))
    else:
        return redirect(url_for("signup"))

@app.route("/users/<username>/")
def user(username):
    db = shelve.get_shelve('r')
    key = "users:{}".format(username)
    if key in db:
        user = db[key]
        return render_template("user.html", user=user)
    else:
        return abort(404)

@app.route("/users/edit/", methods=["GET", "POST"])
def edit_user():
    if request.method == "GET":
        if "username" in session:
            db = shelve.get_shelve('r')
            user = db["users:{}".format(session["username"])]
            return render_template("edit_user.html", user=user)
        else:
            return abort(404)
    else:
        if "username" in session:
            db = shelve.get_shelve('c')
            key = "users:{}".format(session["username"])
            user = db[key]
            for k in ["realname", "email"]:
                user[k] = request.form[k]
            if request.form["newpassword"]:
                if request.form["oldpassword"] == user["password"]:
                    user["password"] = request.form["password"]
            db[key] = user
            return redirect(url_for("user", username=session["username"]))
        else:
            return abort(404)

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
