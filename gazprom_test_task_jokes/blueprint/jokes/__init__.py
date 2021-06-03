from typing import Dict, List

import aiohttp
from sanic import Blueprint, exceptions, HTTPResponse, json, Request
from sanic.log import logger
from sanic_jwt_extended import jwt_required
from sanic_jwt_extended.tokens import Token
from sanic_openapi.openapi2 import doc

from manager import app


class Joke:
    id = doc.String("The unique identifier of your very funny joke.")
    joke = doc.String("Your very funny joke.")
    username = doc.String("The name of your user account.")


jokes = Blueprint('jokes', url_prefix='/jokes')


@jokes.route('/create', methods=['POST'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.consumes(doc.JsonBody({"joke": doc.String("Joke to be created.")}), location="body", required=True)
@doc.produces(Joke)
@doc.response(401, {"msg": str}, description="Unauthorized")
@jwt_required
async def jokes_create(request: Request, token: Token) -> HTTPResponse:
    joke = request.json['joke']
    body = {
        "username": token.identity,
        "joke":     joke,
        }
    
    response = await app.ctx.elasticsearch.index(
        index='jokes',
        body=body
        )
    _id = response['_id']
    return json({"id": _id, "joke": joke, 'username': token.identity}, 201)


@jokes.route('/create_from_geek_jokes', methods=['POST'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.produces(Joke)
@doc.response(401, {"msg": str}, description="Unauthorized")
@jwt_required
async def jokes_create_from_geek_jokes(request: Request, token: Token) -> HTTPResponse:
    async with aiohttp.ClientSession() as session:
        url = 'https://geek-jokes.sameerkumar.website/api'
        async with session.get(url) as resp:
            joke = await resp.text()
            joke = joke.lstrip('"').rstrip('\n').rstrip('"')
    
    body = {
        "username": token.identity,
        "joke":     joke,
        }
    
    response = await app.ctx.elasticsearch.index(
        index='jokes',
        body=body
        )
    _id = response['_id']
    return json({"id": _id, "joke": joke, 'username': token.identity}, 201)


@jokes.route('/read', methods=['GET'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.consumes(doc.String(name="id", description="The unique identifier of your very funny joke."), location="query", required=True)
@doc.response(401, {"msg": str}, description="Unauthorized")
@doc.response(404, {"description": str, "status": int, "message": str}, description="Not Found")
@jwt_required
async def jokes_read(request: Request, token: Token) -> HTTPResponse:
    _id = request.get_args()['id'][0]
    body = {
        "query": {
            "terms": {
                "_id": [_id]
                }
            }
        }
    response = await app.ctx.elasticsearch.search(
        index='jokes',
        body=body
        )
    hits = response['hits']['hits']
    if len(hits) == 0:
        raise exceptions.NotFound("Joke not found.")
    
    source = hits[0]['_source']
    
    username = source['username']
    if username != token.identity:
        raise exceptions.NotFound("Joke not found.")
    
    joke = source['joke']
    return json({"id": _id, "joke": joke, 'username': username}, 200)


@jokes.route('/read_all', methods=['GET'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.produces(doc.List(Joke))
@doc.response(401, {"msg": str}, description="Unauthorized")
@doc.response(404, {"description": str, "status": int, "message": str}, description="Not Found")
@jwt_required
async def jokes_read_all(request: Request, token: Token) -> HTTPResponse:
    body = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "username": token.identity,
                        }
                    }
                }
            }
        }
    response = await app.ctx.elasticsearch.search(
        index='jokes',
        body=body
        )
    hits = response['hits']['hits']
    if len(hits) == 0:
        raise exceptions.NotFound("Jokes not found.")
    jokes: List[Dict[str, str]] = [
        {'id': hit['_id'], 'joke': hit['_source']['joke'], 'username': hit['_source']['username']}
        for hit in hits
        ]
    return json(jokes, 200)


@jokes.route('/update', methods=['PUT'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.consumes(doc.String(name="id", description="The unique identifier of your very funny joke."), location="query", required=True)
@doc.consumes(doc.JsonBody({"joke": doc.String("Joke to be updated.")}), location="body", required=True)
@doc.produces(Joke)
@doc.response(401, {"msg": str}, description="Unauthorized")
@jwt_required
async def jokes_update(request: Request, token: Token) -> HTTPResponse:
    _id = request.get_args()['id'][0]
    joke = request.json['joke']
    
    search_body = {
        "query": {
            "terms": {
                "_id": [_id]
                }
            }
        }
    search_response = await app.ctx.elasticsearch.search(
        index='jokes',
        body=search_body
        )
    hits = search_response['hits']['hits']
    if len(hits) == 0:
        raise exceptions.NotFound("Joke not found.")
    
    username = hits[0]['_source']['username']
    if username != token.identity:
        raise exceptions.NotFound("Joke not found.")
    
    update_body = {
        "doc": {
            "joke": joke
            }
        }
    update_response = await app.ctx.elasticsearch.update(
        index='jokes',
        id=_id,
        body=update_body
        )
    
    return json({"id": _id, "joke": joke, "username": username}, 202)


@jokes.route('/delete', methods=['DELETE'])
@doc.consumes(doc.String(name="Authorization"), location="header", required=True)
@doc.consumes(doc.String(name="id", description="The unique identifier of your very funny joke."), location="query", required=True)
# @doc.produces(Joke)
@doc.response(401, {"msg": str}, description="Unauthorized")
@jwt_required
async def jokes_update(request: Request, token: Token) -> HTTPResponse:
    _id = request.get_args()['id'][0]
    
    search_body = {
        "query": {
            "terms": {
                "_id": [_id]
                }
            }
        }
    search_response = await app.ctx.elasticsearch.search(
        index='jokes',
        body=search_body
        )
    hits = search_response['hits']['hits']
    if len(hits) == 0:
        raise exceptions.NotFound("Joke not found.")
    
    username = hits[0]['_source']['username']
    if username != token.identity:
        raise exceptions.NotFound("Joke not found.")
    
    delete_response = await app.ctx.elasticsearch.delete(
        index='jokes',
        id=[_id]
        )
    
    return json({}, 204)
