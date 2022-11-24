from flask import Blueprint, request
from .db import get_ponds, insert_pond, get_pond, update_pond
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from flask_restful import Api, Resource
from datetime import datetime

bp = Blueprint('pond',__name__)
api = Api(bp)
