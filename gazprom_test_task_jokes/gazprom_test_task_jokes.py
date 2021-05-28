import secure
from elasticsearch import AsyncElasticsearch
from sanic import Blueprint, Sanic
from sanic.log import logger
from sanic_cors import CORS
from sanic_openapi import swagger_blueprint
from sanic_sslify import SSLify
from sanic_useragent import SanicUserAgent

from blueprint.health import health
from util import configure_swagger_ui, setup_rate_limiter

app = Sanic(__name__)

CORS(app)
configure_swagger_ui(app)
SanicUserAgent.init_app(app)
sslify = SSLify(app)
limiter = setup_rate_limiter(app)
secure_headers = secure.Secure()
app.blueprint(swagger_blueprint)

api = Blueprint.group(health, url_prefix="/api", version=1)
app.blueprint(api)


@app.before_server_start
async def setup(app, loop):
    logger.debug('app.before_server_start')
    app.ctx.elastic_search = AsyncElasticsearch([{
        'host': app.config.ELASTICSEARCH_HOST,
        'port': app.config.ELASTICSEARCH_PORT
        }])
    ping = await app.ctx.elastic_search.ping()
    if ping:
        logger.debug('elasticsearch connected')
    else:
        logger.debug('elasticsearch not connected')


@app.after_server_stop
async def teardown(app, loop):
    logger.debug('app.after_server_stop')
    await app.ctx.elastic_search.close()


@app.on_request
async def on_request(request):
    logger.debug('app.on_request')


@app.on_response
async def on_response(request, response):
    logger.debug('app.on_response')
    logger.debug(request.headers)
    logger.debug(response.headers)


@app.on_response
async def set_secure_headers(request, response):
    secure_headers.framework.sanic(response)
    logger.info(str(response.headers))


@app.on_response
async def add_request_id_header(request, response):
    response.headers["X-Request-ID"] = request.id
