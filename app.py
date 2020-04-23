from flask import Flask, jsonify, request
from flask_restful import Api

#importar os Resources, que estao na outra pasta
from Resources.Login import Login
from Resources.Values import Values
from Resources.Keys import Keys


#passando a quem pertence a instancia de Flask
app = Flask(__name__)
#Criando api
api = Api(app)

#Rotas da aplicacao
api.add_resource(Login, '/login')
api.add_resource(Values, '/values')
api.add_resource(Keys, '/keys')

#apenas o arquivo principal pode chamar essa funcao
if __name__ == '__main__':
    app.run(debug=True)
