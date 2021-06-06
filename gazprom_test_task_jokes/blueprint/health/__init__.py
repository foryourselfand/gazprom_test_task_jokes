from sanic import Blueprint
from sanic import HTTPResponse
from sanic import json
from sanic import Request

health = Blueprint('health', url_prefix='/health')


@health.route('/status', methods=['GET'])
async def jokes_create(request: Request) -> HTTPResponse:
    return json({"status": "OK"}, 200)
