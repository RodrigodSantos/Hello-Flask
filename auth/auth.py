from flask_httpauth import HTTPTokenAuth

auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "121314": "rodrigo"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
