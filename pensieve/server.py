#!/usr/bin/python

import sys
import json
import zmq

from .handlers import messageHandlers
from .helpers import checkField, MessageError, typeNotSupported


def dispatchMessage(header, data):
    try:
        type = checkField(header, 'type')
    except MessageError as e:
        return e.json
    if type in messageHandlers:
        return messageHandlers[type].handle(header, data)
    else:
        return typeNotSupported(type)


def startServer():
    host = sys.argv[1] if len(sys.argv) > 1 else "*"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 61455
    proto = sys.argv[3] if len(sys.argv) > 3 else "tcp"
    addr = "{}://{}:{}".format(proto, host, port)

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(addr)

    while True:
        messageFrame = socket.recv(copy=False)
        index = messageFrame.bytes.find("\n")
        print "indexed at ", index
        messageString = str(messageFrame.bytes[:index]) if index > 0 else str(messageFrame.bytes)
        print "messageString: ", messageString
        messageData = messageFrame.bytes[index+1:]
        messageJson = json.loads(messageString)
        socket.send(b"%s" % (dispatchMessage(messageJson, messageData)))

if __name__ == "__main__":
    startServer()
