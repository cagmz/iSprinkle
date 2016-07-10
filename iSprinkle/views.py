#!/usr/bin/python
from iSprinkle import app
from flask import make_response

@app.route('/')
def index():
    return make_response(open('iSprinkle/templates/index.html').read())
