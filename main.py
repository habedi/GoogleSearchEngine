from server.server import TaskServer
from flask import Flask

if __name__ == "__main__":
    app = Flask(__name__)
    ts = TaskServer(flaskapp=app)
    ts.run(host="localhost", port=65000,
           debug=True, use_reloader=False,
           threaded=True)
