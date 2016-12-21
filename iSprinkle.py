import sys
from iSprinkle import app, setup

if __name__ == '__main__':
    setup()
    port = 8081

    if len(sys.argv) == 2:
        try:
            port = int(sys.argv[1])
        except TypeError:
            pass

    app.run(port=port, host='0.0.0.0')
