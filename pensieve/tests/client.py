#!/usr/bin/python

import sys
import zmq
import json

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 61455
proto = sys.argv[3] if len(sys.argv) > 3 else "tcp"
addr = "{}://{}:{}".format(proto, host, port)
message = json.dumps({'type': 'handshake', 'value': 'ping'})
context = zmq.Context()
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect(addr)

print "About to send %s" % (message)
socket.send(b"%s" % (message))

reply = socket.recv()
print("Received reply: %s" % (reply))
