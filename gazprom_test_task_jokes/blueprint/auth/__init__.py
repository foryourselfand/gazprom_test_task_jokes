import dataclasses
from typing import Dict

import bcrypt
from sanic import Blueprint, exceptions, HTTPResponse, json, Request
from sanic.exceptions import Forbidden
from sanic.exceptions import InvalidUsage
from sanic.log import logger
from sanic_jwt_extended import JWT, jwt_required
from sanic_jwt_extended import refresh_jwt_required
from sanic_jwt_extended.tokens import Token
from sanic_openapi.openapi2 import doc

from manager import app
from model import User

auth = Blueprint('auth', url_prefix='/auth')


@auth.route('/register', methods=['POST'])
@doc.consumes(User, location="body", required=True)
@doc.response(201, User, description="Register")
@doc.response(400, {"description": str, "status": int, "message": str}, description="Bad Request")
@doc.response(403, {"description": str, "status": int, "message": str}, description="Forbidden")
async def register(request: Request) -> HTTPResponse:
    if not request.json: raise InvalidUsage("json data is required")
    
    username: str = request.json.get("username", None)
    password: str = request.json.get("password", None)
    if not username or not password: raise InvalidUsage("username and password are required")
    
    user: User = await app.ctx.users_repository.create(
        username=username,
        password=password,
        )
    return json(dataclasses.asdict(user), status=201)


@auth.route('/login', methods=['POST'])
@doc.consumes(User, location="body", required=True)
@doc.response(200, {"Authorization": str}, description="Login")
@doc.response(400, {"description": str, "status": int, "message": str}, description="Bad Request")
@doc.response(401, {"description": str, "status": int, "message": str}, description="Unauthorized")
async def login(request: Request) -> HTTPResponse:
    if not request.json: raise InvalidUsage("json data is required")
    
    username: str = request.json.get("username", None)
    password: str = request.json.get("password", None)
    if not username or not password: raise InvalidUsage("username and password are required")
    
    user: User = await app.ctx.users_repository.read(username=username)
    
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise exceptions.Unauthorized("Password is incorrect.")
    
    refresh_token = JWT.create_refresh_token(identity=username)
    
    return json({"X-Refresh-Token": f'Bearer {refresh_token}'}, status=200)


@auth.route("/logout", methods=["POST"])
@doc.consumes(doc.String(name="X-Refresh-Token"), location="header", required=True)
@doc.response(204, None, description="Logout")
@doc.response(401, {"msg": str}, description="Unauthorized")
@doc.response(422, {"msg": str}, description="Unprocessable Entity")
@refresh_jwt_required
async def logout(request: Request, token: Token) -> HTTPResponse:
    await Token.revoke(token)
    return json({}, status=204)
