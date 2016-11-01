#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, escape
import codecs
app = Flask(__name__)

@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html>
  <head>
    <title>Hola mundo!</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="static/normalize.css">
    <link rel="stylesheet" type="text/css" href="static/main.css">
  <body>
    <div class="wrapper">
    <h1>Práctica 2</h1>
    <h2>Desarrollo de Aplicaciones para Internet</h2>
    <p>En esta página se están cargando los recursos estáticos
    <code>static/normalize.css</code>, <code>static/main.css</code> y <code>static/cat.jpg</code>.</p>
    <img src="static/cat.jpg" alt="Kitten :3">
    <p>Imagen CC BY-SA por <a href="http://flickr.com/photos/nicsuzor/">nicsuzor</a></p>
    <p>Código utilizado:</p>
    <pre><code>{}</code></pre>
    </div>
""".format(escape(codecs.open("2_static.py", "r", "utf-8").read()))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
