from flask_restful import Resource, reqparse, marshal_with, marshal
from model.pessoa import Pessoa, pessoa_fields
from model.menssage import Menssage, msg_fields
from model.endereco import Endereco
from helpers.database import db
from helpers.log.logging import logging
from auth.auth import auth

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str)
parser.add_argument('email', type=str)

class PessoaResource(Resource):

  @marshal_with(pessoa_fields)
  @auth.login_required
  def get(self):
    pessoas = Pessoa.query.all()
    logging.info("Todos os dados listados")
    return pessoas, 201

  @auth.login_required
  def post(self):
    args = parser.parse_args()
    nome = args["nome"]
    email = args["email"]

    pessoa = Pessoa(nome, email)
    db.session.add(pessoa)
    db.session.commit()
    logging.info("Pessoa adicionada!")

    return marshal(pessoa, pessoa_fields), 201
    
      
class PessoaResourceId(Resource):
  @auth.login_required
  def get(self, id):
    pessoa = Pessoa.query.filter_by(id=id).first()
    if pessoa is None:
      logging.error("Pessoa nao encontrada")
      msg = Menssage(1, "Pessoa nao encontrada")
      return marshal(msg, msg_fields), 404
    
    logging.info(f"Pessoa listada! - id:{id}")
    return marshal(pessoa, pessoa_fields), 201
  
  @auth.login_required
  def put(self, id):
    args = parser.parse_args()
    nome = args["nome"]
    email = args["email"]
    
    pessoa = Pessoa.query.filter_by(id=id).first() 

    if pessoa is None:
      msg = Menssage(1, "Pessoa nao encontrada")
      return marshal(msg, msg_fields), 404
  
    pessoa.nome = nome
    pessoa.email = email
    pessoa.status = "activated" 
    db.session.add(pessoa)
    db.session.commit()
    return marshal(pessoa, pessoa_fields), 201
  
  @auth.login_required
  def delete(self, id): 
    pessoa = Pessoa.query.filter_by(id=id).first() 

    if pessoa is None:
      msg = Menssage(1, "Pessoa nao encontrada")
      return marshal(msg, msg_fields), 404
  
    pessoa.status = "disabled"
    db.session.add(pessoa)
    db.session.commit()

    msg = Menssage(200, "Deleted")
    return marshal(msg, msg_fields), 200
  