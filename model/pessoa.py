from flask_restful import fields
from helpers.database import db

pessoa_fields = {"id": fields.Integer, "nome": fields.String, "email": fields.String, "status": fields.String}

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.String, nullable=False)
    
    def __init__(self, nome, email):
      self.nome = nome
      self.email = email
      self.status = "activated"
      
    def __repr__(self):
        return f'<Pessoa {self.nome}>'
