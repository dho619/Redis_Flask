from flask_restful import Resource
from flask import request
from json import dumps
from utils.funcoes import login_Usuario  #funcao implementada em outro arquivo
from db.dbRedis import db


class Login(Resource):
    def post(self):
        data = request.json#busca o json da requisicao
        user = data['user']
        password = data['password']
        usuario, token = login_Usuario(user, password) #criando o token
        if usuario:
            perfil = usuario['perfil']
            #Postar no banco Chave-Valor as informacoes do usuario logado por 3hrs
            key = perfil+':'+token.decode("utf-8")

            value = dumps(usuario)#dicionario para json

            try:
                db.set(key, value, ex=60*60*3)#seg*min*hrs

                return {
                            'status': 'Sucess',
                            'Token': token.decode("utf-8")
                        }
            except Exception as e:
                print(e)
                return {
                            'status': 'Error',
                            'Message': 'Erro ao gravar as informações no Banco'
                       }
        else:
            return {
                        'status': 'Error',
                        'Message': 'Usuario ou senha inválidos'
                    }
