import bcrypt
from sanic import Blueprint, exceptions, HTTPResponse, json, Request
# noinspection PyUnresolvedReferences
from sanic_jwt_extended import JWT, jwt_required, refresh_jwt_required
# noinspection PyUnresolvedReferences
from sanic_jwt_extended.tokens import Token
from sanic_openapi.openapi2 import doc

from manager import app


class User:
    username = str
    password = str


auth = Blueprint('auth', url_prefix='/auth')


@auth.route('/register', methods=['POST'])
@doc.consumes(User, location='body')
@doc.response(403, {"description": str, "status": int, "message": str}, description="Forbidden")
async def register(request: Request) -> HTTPResponse:
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    search_body = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "username": username,
                        }
                    }
                }
            }
        }
    search_response = await app.ctx.elasticsearch.search(
        index='users',
        body=search_body
        )
    hits = search_response['hits']['hits']
    if len(hits) != 0:
        raise exceptions.Forbidden("User with that username already exist.")
    
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    index_body = {
        "username": username,
        "password": password_hashed,
        }
    
    index_response = await app.ctx.elasticsearch.index(
        index='users',
        body=index_body
        )
    return json({'register': "successfully"}, status=201)


@auth.route('/login', methods=['POST'])
@doc.consumes(User, location='body')
@doc.response(401, {"description": str, "status": int, "message": str}, description="Unauthorized")
async def login(request: Request) -> HTTPResponse:
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if not username or not password:
        raise exceptions.Unauthorized("User not found.")
    
    query_body = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "username": username,
                        }
                    }
                }
            }
        }
    response = await app.ctx.elasticsearch.search(
        index='users',
        body=query_body
        )
    hits = response['hits']['hits']
    if len(hits) == 0:
        raise exceptions.Unauthorized("User not found.")
    
    source = hits[0]['_source']
    source_username = source['username']
    source_password = source['password']
    
    if not bcrypt.checkpw(password.encode('utf-8'), source_password.encode('utf-8')):
        raise exceptions.Unauthorized("Password is incorrect.")
    
    access_token = JWT.create_access_token(identity=username)
    
    return json({'login': "successfully", "access_token": access_token}, status=200)


@auth.route("/logout", methods=["POST"])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.response(401, {"msg": str}, description="Unauthorized")
@jwt_required
async def logout(request: Request, token: Token) -> HTTPResponse:
    Token.revoke(token)
    return json({"logout": "successfully"}, status=200)


@auth.route("/protected", methods=["GET"])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.response(401, {"msg": str}, description="Unauthorized")
@jwt_required
async def protected(request: Request, token: Token) -> HTTPResponse:
    return json(dict(identity=token.identity, type=token.type, raw_data=token.raw_data, exp=str(token.exp)), status=200)
