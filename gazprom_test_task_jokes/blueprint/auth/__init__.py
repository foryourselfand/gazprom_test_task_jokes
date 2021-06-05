from typing import Dict

import bcrypt
from sanic import Blueprint, exceptions, HTTPResponse, json, Request
from sanic.log import logger
from sanic_jwt_extended import JWT, jwt_required
from sanic_jwt_extended.tokens import Token
from sanic_openapi.openapi2 import doc

from manager import app
from model import User

auth = Blueprint('auth', url_prefix='/auth')


@auth.route('/register', methods=['POST'])
@doc.consumes(doc.JsonBody({"user": User}), location="body", required=True)
@doc.response(201, None, description="Register")
@doc.response(403, {"description": str, "status": int, "message": str}, description="Forbidden")
async def register(request: Request) -> HTTPResponse:
    user = request.json.get("user")
    await app.ctx.users_repository.create(
        username=user["username"],
        password=user["password"],
        )
    return json({'register': "successfully"}, status=201)


@auth.route('/login', methods=['POST'])
@doc.consumes(doc.JsonBody({"user": User}), location="body", required=True)
@doc.response(200, None, description="Login")
@doc.response(401, {"description": str, "status": int, "message": str}, description="Unauthorized")
async def login(request: Request) -> HTTPResponse:
    user_dict: Dict = request.json.get("user")
    username = user_dict["username"]
    password = user_dict["password"]
    
    user: User = await app.ctx.users_repository.read(
        username=username,
        )
    
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise exceptions.Unauthorized("Password is incorrect.")
    
    access_token = JWT.create_access_token(identity=username)
    
    return json({'login': "successfully", "access_token": f'Bearer {access_token}'}, status=200)


@auth.route("/logout", methods=["POST"])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.response(200, None, description="Logout")
@doc.response(401, {"msg": str}, description="Unauthorized")
@doc.response(422, {"msg": str}, description="Unprocessable Entity")
@jwt_required
async def logout(request: Request, token: Token) -> HTTPResponse:
    await Token.revoke(token)
    return json({"logout": "successfully"}, status=200)
