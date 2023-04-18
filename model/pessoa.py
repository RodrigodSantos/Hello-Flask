from flask_restful import fields
from database import db

pessoa_field = {"id": fields.Integer, "nome": fields.String, "email": fields.String}

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    
    def __init__(self, nome, email):
      self.nome = nome
      self.email = email
      
    def __repr__(self):
        return f'<Pessoa {self.nome}>'      
    
    # @auth.verify_password
    # def authenticate(username, password):
    #     if username and password:
    #         if username == 'Rodrigo' and password == 'rodrigo123':
    #           app.logger.info(f"Acesso permitido para: {username}")
    #           return True
    #     else:
    #       app.logger.info(f"Acesso negado para: {username}")
    #       return False
    #     return False