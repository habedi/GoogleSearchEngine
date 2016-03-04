from server.server import Server
from flask import Flask

if __name__ == "__main__":
    app = Flask(__name__)
    ts = Server(flaskapp=app)
    ts.run(host="localhost", port=65000,
           debug=True, use_reloader=False,
           threaded=True)
