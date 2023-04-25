from flask_restful import fields

msg_fields = {"codigo": fields.Integer, "descricao": fields.String}

class Menssage():
  def __init__(self, codigo, descricao):
     self.codigo = codigo
     self.descricao = descricao
