from flask import Blueprint, request
from .db import get_ponds, insert_pond, get_pond, update_pond
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from flask_restful import Api, Resource
from datetime import datetime

bp = Blueprint('pond',__name__)
api = Api(bp)


class Ponds(Resource):
    def get(self):
        data = get_ponds()
        return json.loads(dumps(data))
    
    def post(self):
        today = datetime.now().strftime("%d/%m/%Y")
        req = request.json
        data = {
            'name':req.get('nama'),
            'location':req.get('lokasi'),
            'material':req.get('material'),
            'shape':req.get('bentuk'),
            'number':req.get('nomor'),
            'diameter':int(req.get('diameter')),
            'height':int(req.get('tinggi')),
            'total_fish':int(req.get('jumlah_ikan')),
            'is_active':False,
            'created_at': today
        }
        insert_pond(data)
        return {'success':True}

api.add_resource(Ponds, '/API/ponds')


class Pond(Resource):
    def get(self, pond_id):
        ObjInstance = ObjectId(pond_id)
        filter = {'_id':ObjInstance}
        data = get_pond(filter)
        return json.loads(dumps(data))
    
    def put(self, pond_id):
        ObjInstance = ObjectId(pond_id)
        filter = {'_id':ObjInstance}
        req = request.form
        newvalues ={"$set":{
           'name':req.get('nama'),
            'location':req.get('lokasi'),
            'material':req.get('material'),
            'shape':req.get('bentuk'),
            'number':req.get('nomor'),
            'diameter':int(req.get('diameter')),
            'height':int(req.get('tinggi')),
            'total_fish':int(req.get('jumlah_ikan')), 
        }}
        update_pond(filter,newvalues)
        return {"success":True}

api.add_resource(Pond, '/API/pond/<pond_id>')
