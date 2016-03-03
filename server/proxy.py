from .internals.debug import print_stack_trace
from .internals.constants import proxy_test_urls, proxy_timeout
from random import choice
import socket


class Proxy(object):
    def __init__(self, proxy):
        if not isinstance(proxy, (list, tuple)):
            return -1331
        if len(proxy) != 2:
            return -1332
        try:
            import socks
            import socket

            ip, port = proxy
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
        except:
            print_stack_trace()
            return -1333
        else:
            self.proxy = proxy
        finally:
            pass

    def get_proxy(self):
        return self.proxy

    def test_proxy(self, timeout, url):

        # for neurilizing side effect caused by "socket.socket = socks.socksocket"
        prev_state = socket.socket
        try:
            import socks
            import requests

            ip, port = self.proxy
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
            socket.socket = socks.socksocket
            res = requests.get(url, timeout=timeout)
        except:
            print_stack_trace()
            socket.socket = prev_state
            return -1334
        else:
            socket.socket = prev_state
            if not res.ok:
                return -1335
            else:
                return "Ok"


if __name__ == "__main__":
    try:
        p = Proxy(proxy=("0.0.0.0", 1080))
        tr = p.test_proxy(timeout=proxy_timeout, url=choice(proxy_test_urls))
    except:
        print_stack_trace()
    else:
        if isinstance(p, (int)) and p < 0:
            print("error code", p)
        else:
            if isinstance(tr, (int)) and tr < 0:
                print("error code", tr)
            else:
                print(p.get_proxy())
