import errno
import random
import re
import requests
import socket
import time

import socks

# colour stacktrace printing
from .internals.debug import print_stack_trace

# importing the global constants
from .internals.constants import websearch_timeout

# random time slice generator determines the time slices needed in between each query to be sent to Yahoo
from .internals.ts_generator import generate_random_tses


class search_google(object):
    def __init__(self, proxy=None):
        self.server = "www.google.com"
        self.headers = {
            "User-Agent": "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"}
        self.quantity = "100"
        self.proxy = proxy

    def _do_search(self, term, start=0):
        try:

            if self.proxy and isinstance(self.proxy, (tuple, list)) and len(self.proxy) == 2:
                ip, port = self.proxy
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
                socket.socket = socks.socksocket

            # construtting the request format
            urly = "http://" + self.server + "/search?num=" + "100" + "&start=" + str(start) + \
                   "&hl=en&meta=&q=" + requests.utils.quote(term)

        except:
            print_stack_trace()
            return -1201
        else:
            try:
                r = requests.get(urly, headers=self.headers, timeout=websearch_timeout)
            except Exception as err:
                if (err.errno in (errno.ECONNABORTED, errno.ECONNREFUSED,
                                  errno.ECONNRESET, errno.ECOMM)) or \
                                requests.exceptions.ConnectionError.errno is err or \
                                requests.exceptions.Timeout.errno is err:
                    return -1370
                else:
                    print_stack_trace()
                    return -1202
            else:
                try:
                    raw_results = r.text.encode("utf-8")
                    url_results = []
                    r = re.findall('href="/url\?q=(.+?)">', raw_results.decode('utf8'), flags=re.I)
                    for item in r:
                        if 'webcache.googleusercontent.com' not in item:
                            nr = re.findall('(.+)&amp;sa=U', item, flags=re.I)
                            if len(nr) > 0:
                                url_results.append(nr[0].strip())
                except:
                    print_stack_trace()
                    return -1203
                else:
                    return url_results
        return []


class GoogleSearch(search_google):
    def _getURLs(self, term, num_results):
        results = []
        prev_res = 0
        active = True
        res = [None]
        x = 0
        quotient = ((num_results / 50) + 1)
        while len(results) < num_results and \
                (isinstance(res, (list, tuple)) and not len(res) < 1):
            ts = random.choice(generate_random_tses())
            time.sleep(ts)
            try:
                res = self._do_search(term, start=(x * 10 + 1))
            except:
                print_stack_trace()
                return -1326
            else:
                if isinstance(res, (int)) and res < 0:
                    return res
                else:
                    results += res
                    results = list(set(results))
                    len(results)
                    x += 1

                    if active:
                        prev_res = len(results)
                        active = False
                    else:
                        if prev_res == len(results):
                            break
                        else:
                            prev_res = len(results)

        if len(results) <= num_results:
            return list(results)
        else:
            return list(results)[:num_results]

    def fetchURLs(self, term, num_results):
        try:
            urls = self._getURLs(term, int(num_results))
        except:
            print_stack_trace()
            return -1301
        else:
            if isinstance(urls, (int)) and urls < 0:
                return urls
            else:
                if len(urls) > 0:
                    return urls
                else:
                    return []


if __name__ == "__main__":
    search = GoogleSearch(proxy=None)
    c = 0
    res = search.fetchURLs(term="time", num_results=53)
    if isinstance(res, (int)) and res < 0:
        print("error code", res)
    else:
        for i in res:
            c += 1
            print(i, c)
