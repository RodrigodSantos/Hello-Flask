from flask_restful import Resource, reqparse, marshal_with, marshal
from model.pessoa import Pessoa, pessoa_field
from model.menssage import Menssage
from database import db

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str)
parser.add_argument('email', type=str)

class PessoaResource(Resource):

  @marshal_with(pessoa_field)
  def get(self):
    pessoas = Pessoa.query.all()
    return pessoas, 201

  @marshal_with(pessoa_field)
  def post(self):
    args = parser.parse_args()
    nome = args["nome"]
    email = args["email"]
    
    pessoas = Pessoa(nome, email)
    
    db.session.add(pessoas)
    db.session.commit()
    
    return pessoas, 201
      
class PessoaResourceId(Resource):

  @marshal_with(pessoa_field)
  def get(self, id):
    pessoa = Pessoa.query.filter_by(id=id).first()
    if pessoa is not None:
      return marshal(pessoa, pessoa_field), 201
    else:
      msg = Menssage("Pessoa nao encontrada", 1)
      return marshal(msg, pessoa_field), 404
    
  @marshal_with(pessoa_field)
  def put(self, id):
    args = parser.parse_args()
    nome = args["nome"]
    email = args["email"]
    
    pessoa = Pessoa.query.get(id)
    
    if pessoa is not None:
      pessoa.nome = nome
      pessoa.email = email
      
      db.session.add(pessoa)
      db.session.commit()
      return marshal(pessoa, pessoa_field), 201
    
    else:
      msg = Menssage("Pessoa nao encontrada", 1)
      return marshal(msg, pessoa_field), 404
  def delete(self, id):
    return