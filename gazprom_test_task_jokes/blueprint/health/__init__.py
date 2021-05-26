from sanic import Request
from sanic_openapi import doc

from sanic.blueprints import Blueprint
from sanic.response import HTTPResponse, json

health = Blueprint("health", url_prefix="/health", version=1)


@health.route("/status")
@doc.summary("Health Status API")
@doc.produces({"status": str})
async def health_status_swagger(request: Request) -> HTTPResponse:
    return json({"status": "OK"})
