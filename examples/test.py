from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi
import gevent


# demo app
import os
import string

import random
import pdb

from datetime import datetime

def handle(ws, payload_size=1024, delay=0.1, num_messages=100):
    """  This is the websocket handler function.  Note that we
    can dispatch based on path in here, too."""
    if ws.path == '/echo':
        while True:
            m = ws.wait()
            if m is None:
                break
            ws.send(m)

    elif ws.path == '/data':
        payload_size = int(payload_size)
        delay = float(delay)
        num_messages = int(num_messages)
        
        delay = delay / 1000.0
        print 'using payload: %d, delay: %f, num messages: %d' % (payload_size, delay, num_messages)
        
        for i in xrange(num_messages):
            now = datetime.now()
            payload = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(payload_size))
            
            msg = '%d|%d|%d|%d|%d|%d|%d|%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second, int(now.microsecond/1000.0), payload)
#            print 'sending msg: ', msg
#            ws.send("0 %s %s\n" % (i, msg))
#            ws.send(msg)
#            msg = "0 %s %s\n" % (i, random.random())
#            print 'msg: %s' % msg
#            print 'msg: %d' % i
#            print 'payload length: %d' % len(payload)
            ws.send(msg)
            
#            print 'sleeping for %f\n' % delay
            gevent.sleep(delay)


def app(environ, start_response):
    if environ['PATH_INFO'] == '/status':
        start_response("200 OK", [('Content-Type', 'text/plain')])
        return ["websocket server is running"]
    elif environ['PATH_INFO'] == "/data":
        query = environ['QUERY_STRING'].split('&')
        payload_size = 1024
        delay = 0.1
        num_messages = 100
        
        for q in query:
            if 'payload_size' in q:
                payload_size = q.split('=')[-1]
            if 'delay' in q:
                delay = q.split('=')[-1]
            if 'num_messages' in q:
                num_messages = q.split('=')[-1]
        
        handle(environ['wsgi.websocket'], payload_size, delay, num_messages)
    else:
        start_response("404 - path not found. Available paths: /status and /data", [])
        return []



server = pywsgi.WSGIServer(('127.0.0.1', 8001), app,
        handler_class=WebSocketHandler)
print 'waiting for connection...'
server.serve_forever()

