from flask_restful import fields
from helpers.database import db

pessoa_fields = {
}

class Endereco(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa.id'))

    def __init__(self):
      pass
      
    def __repr__(self):
        return f'<Endereco>'