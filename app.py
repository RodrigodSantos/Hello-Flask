from flask import Flask, Blueprint
from flask_restful import Api
from helpers.database import db, migrate
from helpers import cors
from resources.pessoa import PessoaResource, PessoaResourceId

app = Flask(__name__)

api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix="/api")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
cors.__init__("app")
migrate.__init__(app, db)

api.add_resource(PessoaResource, '/pessoa')
api.add_resource(PessoaResourceId, '/pessoa/<int:id>')
app.register_blueprint(api_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
