import json


class MessageError(Exception):
    def __init__(self, json=None):
        self.json = json


def ok(type, value):
    return json.dumps({'status': 200, 'type': type, 'value': value})


def errorMessage(status, message):
    return json.dumps({'status': status, 'type': 'error', 'message': message})


def missingField(field):
    return errorMessage(400, "Expecting (%s) field." % (field))


def invalidValue(field, value=None, expecting=None):
    expectString = ""
    if expecting is not None:
        expectString = "Was expecting %s." % (expecting)
    return errorMessage(400, "Invalid value (%s) for field (%s). %s" % (value, field, expectString))


def typeNotSupported(type):
    return errorMessage(403, "Type (%s) not supported." % (type))


def checkField(message, field):
    if field not in message:
        raise MessageError(json=missingField(field))
    return message[field]


def checkValue(message, field, expectedValue, returnValue=None):
    value = checkField(message, field)
    if value != expectedValue:
        raise MessageError(json=invalidValue(field, message[field], expectedValue))

    return returnValue
