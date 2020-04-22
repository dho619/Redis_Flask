import redis, json
from flask import Flask, jsonify, request

from funcoes import login_Usuario#funcao implementada em outro arquivo

db = redis.Redis(host='localhost')#criando o ligamento com o banco REDIS

app = Flask(__name__)#passando a quem pertence a instancia de Flask

@app.route('/login', methods=['POST']) #criando uma rota post
def login():
    response = json.loads(request.data)#transformando em json
    user = response['user']
    password = response['password']
    usuario, token = login_Usuario(user, password) #criando o token

    if usuario:
        perfil = usuario['perfil']

        #Postar no banco Chave-Valor as informacoes do usuario logado por 3hrs
        key = perfil+':'+token.decode("utf-8")
        value = json.dumps(usuario)#dicionario para json
        try:
            db.set(key, value, ex=60*60*3)#seg*min*hrs
        except Exception as e:
            print(e)
            return jsonify({
                            'status': 'Error',
                            'Message': 'Erro ao gravar as informações no Banco'
                           })

        return jsonify({
                        'status': 'Sucess',
                        'Token': token
                       })
    else:
        return jsonify({
                        'status': 'Error',
                        'Message': 'Usuario ou senha inválidos'
                       })

@app.route('/getValue', methods=['GET'])
def getValue():
    body = json.loads(request.data)
    #O usuario esta buscando um valor especifico
    if 'key' in body:
        key = body['key']
        return db.get(key)
    #O usuario passar parte da chave, e ira receber tds com essa chave
    elif 'key_f' in body:
        key_f= body['key_f']
        keys = db.keys(key_f+'*')

        #pegando os valores a partir das chaves e colocando em um array de dicionarios
        values = [json.loads(db.get(key.decode('utf-8'))) for key in keys]
        return jsonify(values)
    else:
        return jsonify({
                        'status': 'Error',
                        'Message': 'Esperado os parametros key ou key_f'
                       })

@app.route('/lista', methods=['GET'])
def listar():
    return jsonify(db.keys('*'))


if __name__ == '__main__':
    app.run(debug=True)
