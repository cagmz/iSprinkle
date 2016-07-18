#!/usr/bin/python
from iSprinkle import app, setup
from flask import g
import sqlite3, os


# database = '/data/database.db'
#
#
# def setup_database():
#     default_config = dict(DATABASE=os.path.join(app.root_path, database),
#                           SECRET_KEY='development key', USERNAME='admin',
#                           PASSWORD='default')
#     app.config.update(default_config)
#
#
# def connect_database():
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv
#
#
# def get_db():
#     """comments"""
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_database()
#     return g.sqlite_db
#
#
#
# @app.teardown_appcontext
# def close_db(error)
#     """more comments"""
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_database()
#     return g.sqlite_db


if __name__ == '__main__':
    # setup_database()
    setup()
    app.run(host='0.0.0.0')
