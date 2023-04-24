from flask_httpauth import HTTPTokenAuth
from log.logging import logging

auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "121314": "rodrigo"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        logging.info(f"Alteracao feita - token:{token}")
        return tokens[token]
