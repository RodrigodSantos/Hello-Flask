from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from database import db
from resources.pessoa import PessoaResource, PessoaResourceId
import logging


app = Flask(__name__)
# auth = HTTPBasicAuth()

api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix="/api")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.basicConfig(
  level=logging.DEBUG, 
  format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
  handlers=[
    logging.FileHandler("info.log", mode='w'),logging.StreamHandler()
  ]
)

db.init_app(app)
with app.app_context():
  db.create_all()
  
api.add_resource(PessoaResource, '/pessoa')
api.add_resource(PessoaResourceId, '/pessoa/<int:id>')
app.register_blueprint(api_bp)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
      