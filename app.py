from flask import Flask, Blueprint
from flask_restful import Resource, Api, reqparse, marshal_with, fields, marshal
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
import logging


# create the app
app = Flask(__name__)
auth = HTTPBasicAuth()
# create the extension
db = SQLAlchemy()
# restful
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix="/api")

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.basicConfig(
  level=logging.DEBUG, 
  format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
  handlers=[
    logging.FileHandler("info.log", mode='w'),logging.StreamHandler()
  ]
)

# initialize the app with the extension
db.init_app(app)

pessoa_field = {"id": fields.Integer, "nome": fields.String, "email": fields.String}
parser = reqparse.RequestParser()
parser.add_argument('nome', type=str)
parser.add_argument('email', type=str)

class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    
    def __init__(self, nome, email):
      self.nome = nome
      self.email = email
      
    def __repr__(self):
        return f'<Pessoa {self.nome}>'      
    
    @auth.verify_password
    def authenticate(username, password):
        if username and password:
            if username == 'Rodrigo' and password == 'rodrigo123':
              app.logger.info(f"Acesso permitido para: {username}")
              return True
        else:
          app.logger.info(f"Acesso negado para: {username}")
          return False
        return False
    
class Menssage():
  def __init__(self, codigo, descricao):
     self.codigo = codigo
     self.descricao = descricao  

class PessoaResource(Resource):

  @marshal_with(pessoa_field)
  def get(self):
    pessoas = Pessoa.query.all()
    return pessoas, 201

  @marshal_with(pessoa_field)
  @auth.login_required
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
  @auth.login_required
  def get(self, id):
    pessoa = Pessoa.query.filter_by(id=id).first()
    if pessoa is not None:
      return marshal(pessoa, pessoa_field), 201
    else:
      msg = Menssage("Pessoa nao encontrada", 1)
      return marshal(msg, pessoa_field), 404
    
  @marshal_with(pessoa_field)
  @auth.login_required
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

with app.app_context():
  db.create_all()
  
api.add_resource(PessoaResource, '/pessoa')
api.add_resource(PessoaResourceId, '/pessoa/<int:id>')
app.register_blueprint(api_bp)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
      