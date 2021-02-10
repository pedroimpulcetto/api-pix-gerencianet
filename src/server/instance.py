from flask import Flask
from flask_restplus import Api, Resource, fields
import ssl

class Server(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app, 
            version='1.0', 
            title='API PIX Gerencianet',
            description='API para gerar pagamentos dinamicos.', 
            doc='/docs'
        )
        
    def run(self):
        self.app.run(
                debug=True,
            )

server = Server()