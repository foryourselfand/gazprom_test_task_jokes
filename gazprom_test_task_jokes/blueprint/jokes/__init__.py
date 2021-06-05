import dataclasses
from typing import List

import aiohttp
from sanic import Blueprint, HTTPResponse, Request, json
from sanic_jwt_extended import jwt_required
from sanic_jwt_extended.tokens import Token
from sanic_openapi.openapi2 import doc

from manager import app
from model import Joke

jokes = Blueprint('jokes', url_prefix='/jokes')


@jokes.route('/create', methods=['POST'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.consumes(doc.JsonBody({"joke": doc.String("Joke to be created.")}), location="body", required=True)
@doc.response(201, Joke, description="Create")
@doc.response(401, {"msg": str}, description="Unauthorized")
@doc.response(422, {"msg": str}, description="Unprocessable Entity")
@jwt_required
async def jokes_create(request: Request, token: Token) -> HTTPResponse:
    joke: Joke = await app.ctx.jokes_repository.create(
        username=token.identity,
        joke=request.json['joke'],
        )
    return json(dataclasses.asdict(joke), 201)


@jokes.route('/create_from_geek_jokes', methods=['POST'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.response(201, Joke, description="Create")
@doc.response(401, {"msg": str}, description="Unauthorized")
@doc.response(422, {"msg": str}, description="Unprocessable Entity")
@jwt_required
async def jokes_create_from_geek_jokes(request: Request, token: Token) -> HTTPResponse:
    url: str = 'https://geek-jokes.sameerkumar.website/api'
    async with app.ctx.client_session.get(url) as resp:
        joke: str = await resp.text()
        joke = joke.lstrip('"').rstrip('\n').rstrip('"')
    
    joke: Joke = await app.ctx.jokes_repository.create(
        username=token.identity,
        joke=joke,
        )
    return json(dataclasses.asdict(joke), 201)


@jokes.route('/read', methods=['GET'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.consumes(doc.String(name="id", description="The unique identifier of your very funny joke."), location="query", required=True)
@doc.response(200, Joke, description="Read")
@doc.response(401, {"msg": str}, description="Unauthorized")
@doc.response(404, {"description": str, "status": int, "message": str}, description="Not Found")
@doc.response(422, {"msg": str}, description="Unprocessable Entity")
@jwt_required
async def jokes_read(request: Request, token: Token) -> HTTPResponse:
    joke: Joke = await app.ctx.jokes_repository.read(
        _id=request.get_args()['id'][0],
        username=token.identity,
        )
    return json(dataclasses.asdict(joke), 200)


@jokes.route('/read_all', methods=['GET'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.response(200, List[Joke], description="Read")
@doc.response(401, {"msg": str}, description="Unauthorized")
@doc.response(404, {"description": str, "status": int, "message": str}, description="Not Found")
@doc.response(422, {"msg": str}, description="Unprocessable Entity")
@jwt_required
async def jokes_read_all(request: Request, token: Token) -> HTTPResponse:
    jokes_list: List[Joke] = await app.ctx.jokes_repository.read_all(username=token.identity)
    return json([
        dataclasses.asdict(jokes_element)
        for jokes_element in jokes_list
        ]
        , 200)


@jokes.route('/update', methods=['PUT'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.consumes(doc.String(name="id", description="The unique identifier of your very funny joke."), location="query", required=True)
@doc.consumes(doc.JsonBody({"joke": doc.String("Joke to be updated.")}), location="body", required=True)
@doc.response(202, Joke, description="Update")
@doc.response(401, {"msg": str}, description="Unauthorized")
@doc.response(404, {"description": str, "status": int, "message": str}, description="Not Found")
@doc.response(422, {"msg": str}, description="Unprocessable Entity")
@jwt_required
async def jokes_update(request: Request, token: Token) -> HTTPResponse:
    joke: Joke = await app.ctx.jokes_repository.update(
        _id=request.get_args()['id'][0],
        username=token.identity,
        joke=request.json['joke'],
        )
    return json(dataclasses.asdict(joke), 202)


@jokes.route('/delete', methods=['DELETE'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.consumes(doc.String(name="id", description="The unique identifier of your very funny joke."), location="query", required=True)
@doc.response(204, None, description="Delete")
@doc.response(401, {"msg": str}, description="Unauthorized")
@doc.response(404, {"description": str, "status": int, "message": str}, description="Not Found")
@doc.response(422, {"msg": str}, description="Unprocessable Entity")
@jwt_required
async def jokes_delete(request: Request, token: Token) -> HTTPResponse:
    await app.ctx.jokes_repository.delete(
        _id=request.get_args()['id'][0],
        username=token.identity,
        )
    return json({}, 204)
