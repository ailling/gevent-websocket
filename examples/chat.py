from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi
import gevent


# demo app
import os
import string

import random
import pdb

from datetime import datetime

IP = '69.67.30.76'

def handle(ws):
    """  This is the websocket handler function.  Note that we
    can dispatch based on path in here, too."""
    if ws.path == '/echo':
        while True:
            m = ws.wait()
            if m is None:
                break
            ws.send(m)
    
    elif ws.path == '/chat':
        ws.send('connected')
        try:
            while True:
                message = ws.receive()
                if message is None:
                    ws.close()
                    break
                else:
                    ws.send('you said: ' + message)
        finally:
            ws.close()



def app(environ, start_response):
    if environ['PATH_INFO'] == '/status':
        start_response("200 OK", [('Content-Type', 'text/plain')])
        return ["websocket server is running"]
    elif environ['PATH_INFO'] == "/chat":
        handle(environ['wsgi.websocket'])
    else:
        start_response("404 - path not found. Available paths: /status and /chat", [])
        return []



server = pywsgi.WSGIServer((IP, 8001), app, handler_class=WebSocketHandler)
print 'waiting for connection...'
server.serve_forever()

