from flask import request

def getJsonField(field, required = None):
    try:
        data = request.json[field]
        return data
    except Exception as error:
        return None
