import json

from flask import Flask
from flask import request, jsonify

from .internals.debug import print_stack_trace
from .internals.errors import *


class Server(object):
    def __init__(self, flaskapp):
        self.app = flaskapp

    def run(self, host, port, debug=True, use_reloader=False, threaded=False):

        @self.app.route('/gsearch', methods=['POST'])
        def handleGoogleSearches():

            if request.headers['Content-Type'] == 'application/json' and \
                            len(str(request.data, "utf-8")) > 0:
                try:
                    from server.googlesearch import GoogleSearch
                    search = GoogleSearch(proxy=None)
                    body = json.loads(str(request.data, "utf-8"))
                    res = search.fetchURLs(term=body["term"],
                                           num_results=int(body["nresults"]))
                except:
                    print_stack_trace()
                    return (jsonify(error=errors[SERVICE_UNKNOWN_ERROR]),
                            SERVICE_UNKNOWN_ERROR)
                else:
                    if isinstance(res, (int)) and res < 0:
                        return (jsonify(error=errors[res]),
                                res)
                    else:
                        return (jsonify(ok={"results": res}),
                                200)
            else:
                return (jsonify(error=errors[SERVICE_INVALID_REQUEST_FORMAT]),
                        SERVICE_INVALID_REQUEST_FORMAT)

        self.app.run(host=host, port=port, debug=debug,
                     use_reloader=use_reloader, threaded=threaded)


if __name__ == "__main__":
    app = Flask(__name__)
    ts = Server(flaskapp=app)
    ts.run(host="0.0.0.0", port=65000,
           debug=True, use_reloader=False,
           threaded=True)
