from flask_restful import Resource
from flask import jsonify
from db.dbRedis import db

class Keys(Resource):
    def get(self):
        return jsonify(db.keys('*')) #jsonify transforma em json
