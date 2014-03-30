from .base_handler import BaseHandler
from ..helpers import ok, checkValue, MessageError


class Handshake(BaseHandler):
    def handle(self, header, data):
        try:
            return checkValue(header, 'value', 'ping', ok('handshake', 'pong'))
        except MessageError as e:
            print "Got exception: ", e
            return e.json
