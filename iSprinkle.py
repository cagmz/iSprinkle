from iSprinkle import app, setup

# database = '/data/database.db'


if __name__ == '__main__':
    setup()
    app.run(port=8080, host='0.0.0.0')
