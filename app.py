#!/usr/bin/python
from flask import Flask, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return make_response(open('templates/index.html').read())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
