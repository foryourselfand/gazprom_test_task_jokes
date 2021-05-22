from gazprom_test_task_jokes.blueprint.health import health
from gazprom_test_task_jokes.util import setup_rate_limiter
from sanic_openapi import doc, swagger_blueprint

from sanic import Sanic
from sanic.response import json

app = Sanic(__name__)

limiter = setup_rate_limiter(app)

app.blueprint(swagger_blueprint)

app.blueprint(health)


@app.route("/")
async def default(request):
    return json({"message": "hello Sanic!"})
