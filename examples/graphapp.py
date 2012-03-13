from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi
import gevent


# demo app
import os
import string

import random
import pdb

from datetime import datetime

def handle(ws, delay=0.1, num_messages=100):
    """  This is the websocket handler function.  Note that we
    can dispatch based on path in here, too."""
    if ws.path == '/echo':
        while True:
            m = ws.wait()
            if m is None:
                break
            ws.send(m)
    
    elif ws.path == '/graph-data':
        delay = float(delay)
        num_messages = int(num_messages)
        delay = delay / 1000.0
        
        for i in xrange(num_messages):
            msg = '%s' % random.random()
            ws.send(msg)
            gevent.sleep(delay)


def app(environ, start_response):
    if environ['PATH_INFO'] == '/status':
        start_response("200 OK", [('Content-Type', 'text/plain')])
        return ["websocket server is running"]
    elif environ['PATH_INFO'] == "/graph-data":
        query = environ['QUERY_STRING'].split('&')
        delay = 0.1
        num_messages = 100
        
        for q in query:
            if 'delay' in q:
                delay = q.split('=')[-1]
            if 'num_messages' in q:
                num_messages = q.split('=')[-1]
        
        handle(environ['wsgi.websocket'], delay, num_messages)
    else:
        start_response("404 - path not found. Available paths: /status and /data", [])
        return []



server = pywsgi.WSGIServer(('127.0.0.1', 8001), app,
        handler_class=WebSocketHandler)
print 'waiting for connection...'
server.serve_forever()

