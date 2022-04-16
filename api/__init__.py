from flask import Blueprint
import json

bp = Blueprint('api', __name__)
from api import employees


def decode_json(data):
    data = data.response
    data = [json.loads(i) for i in data if i]
    return data