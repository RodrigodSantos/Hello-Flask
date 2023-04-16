import sqlite3
from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal_with, fields, marshal
import logging

app = Flask(__name__)
api = Api(app)


logging.basicConfig(
  level=logging.DEBUG, 
  format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
  handlers=[
    logging.FileHandler("info.log", mode='w'),logging.StreamHandler()
  ]
)

PessoaField = {"id": fields.Integer, "nome": fields.String, "created": fields.String, "email": fields.String}

PessoaErroField = {"codigo": fields.Integer, "descricao": fields.String}

class Menssage():
  def __init__(self, codigo, descricao):
     self.codigo = codigo
     self.descricao = descricao


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

parser = reqparse.RequestParser()
parser.add_argument('nome', type=str)
parser.add_argument('email', type=str)
    
class Pessoas(Resource):

  @marshal_with(PessoaField)
  def get(self):

    try:
       
      conn = get_db_connection()
      cur = conn.cursor()
      pessoas_db = cur.execute('SELECT * FROM pessoas').fetchall()
      
      app.logger.info("Clientes listados")


    except:
       
       app.logger.error("Não foi possivel listar os clientes")

    finally:
      conn.close()

    return pessoas_db

  @marshal_with(PessoaField)
  def post(self):

    try:

      args = parser.parse_args()
      conn = get_db_connection()
      cur = conn.cursor()

      insert = cur.execute("INSERT INTO pessoas (nome, email) VALUES(?, ?)",(args["nome"], args["email"]))
      conn.commit()

      app.logger.info("Cliente criado com sucesso!")

      pessoa = cur.execute(
        "SELECT * FROM pessoas WHERE id = ?",(insert.lastrowid,)
      ).fetchall()
      
    except:
        conn().rollback()
        app.logger.error(f"Não foi possível criar o cliente")

    finally:
        conn.close()
        return pessoa, 201
        
    
    
class Pessoa_id(Resource):

  def get(self, id):
    try:
      conn = get_db_connection()
      cur = conn.cursor()      
      select = cur.execute("select * from pessoas where id = ?", (id,)).fetchone()
            
      if not select:
        app.logger.error(f"Cliente de id {id} nao encontrado")
        msg = Menssage(1, "Nao possivel mostrar o cliente!")
        return marshal(msg, PessoaErroField)
      
      app.logger.info(f"Cliente encontrado -> id: {id}")
      return marshal(select, PessoaField), 200
    
    except:
      app.logger.error(f"Cliente de id {id} não encontrado")

    finally:
      conn.close()

  def put(self, id):
    try:
      args = parser.parse_args()
      conn = get_db_connection()
      cur = conn.cursor()      
      verify = cur.execute("select * from pessoas where id = ?", (id,)).fetchone()
      
      if not verify:
        app.logger.error(f"Cliente de id {id} nao encontrado")
        msg = Menssage(1, "Nao possivel encontrar o cliente!")
        return marshal(msg, PessoaErroField)

      cur.execute("UPDATE pessoas SET nome = ?, email = ? WHERE id = ?", (args["nome"], args["email"], id))
      conn.commit()
      app.logger.info(f"Cliente de id:{id} atualizado!")

      select = cur.execute("select * from pessoas where id = ?", (id,)).fetchone()


      return marshal(select, PessoaField)
    finally:
      conn.close()

  def delete(self, id):
      try:
        conn = get_db_connection()
        cur = conn.cursor()      
        select = cur.execute("select * from pessoas where id = ?", (id,)).fetchone()
        
        if not select:
          app.logger.error(f"Cliente de id {id} nao encontrado")
          msg = Menssage(1, "Nao possivel encontrar o cliente!")
          return marshal(msg, PessoaErroField)
        
        cur.execute("DELETE FROM pessoas WHERE id=?", (id,))
        conn.commit()

        
        return " "
        
      finally:
        conn.close()

  
         


api.add_resource(Pessoas, '/pessoas')
api.add_resource(Pessoa_id, '/pessoas/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)