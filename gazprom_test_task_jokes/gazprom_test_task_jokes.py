from gazprom_test_task_jokes.blueprint.health import health
from gazprom_test_task_jokes.util import setup_rate_limiter
from sanic_openapi import doc, swagger_blueprint

from sanic import Blueprint, Request, Sanic
from sanic.response import HTTPResponse, json, text

app = Sanic(__name__)

limiter = setup_rate_limiter(app)

app.blueprint(swagger_blueprint)
api = Blueprint.group(health, url_prefix="/api", version=1)
app.blueprint(api)


@app.before_server_start
async def setup_db(app, loop):
    pass


@app.after_server_stop
async def teardown_db(app, loop):
    pass


@app.on_request
async def extract_user(request):
    # request.ctx.user = await extract_user_from_request(request)
    pass


@app.on_response
async def prevent_xss(request, response):
    response.headers["x-xss-protection"] = "1; mode=block"


@app.on_response
async def add_request_id_header(request, response):
    response.headers["X-Request-ID"] = request.id


@app.route("/check_Token_or_Bearer")
async def handler(request):
    return text(str(request.token))


@app.route("/check_X-Request-ID")
async def handler(request):
    return text(str(request.id))
