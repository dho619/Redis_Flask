from flask_restful import Resource
from flask import request
from json import loads
from db.dbRedis import db

class Values(Resource):
    def get(self):
        data = request.json
        #O usuario esta buscando um valor especifico
        if 'key' in data:
            key = data['key']
            return loads(db.get(key))#string para json
        #O usuario passa parte da chave, e ira receber tds com essa chave
        elif 'key_f' in data:
            key_f= data['key_f']
            keys = db.keys(key_f+'*')

            #pegando os valores a partir das chaves e colocando em um array de dicionarios
            values = [loads(db.get(key.decode('utf-8'))) for key in keys]
            return (values)
        else:
            return {
                        'status': 'Error',
                        'Message': 'Esperado os parametros key ou key_f no corpo da requisicao'
                   }
