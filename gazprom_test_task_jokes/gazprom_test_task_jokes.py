import asyncio

import aiohttp
from elasticsearch import AsyncElasticsearch
from sanic import Blueprint
from sanic.log import logger

from manager import app
from manager import secure_headers
from repository.jokes.elasticsearch import JokesRepositoryElasticsearch
from repository.users.elasticsearch import UsersRepositoryElasticsearch
from route.auth import auth
from route.health import health
from route.jokes import jokes

api = Blueprint.group(auth, jokes, health, url_prefix="/api", version=1)
app.blueprint(api)


@app.before_server_start
async def before_server_start(app, loop):
    logger.debug('app.before_server_start')
    
    app.ctx.elasticsearch = AsyncElasticsearch([{
        'host': app.config.ELASTICSEARCH_HOST,
        'port': app.config.ELASTICSEARCH_PORT
        }])
    
    while True:
        ping = await app.ctx.elasticsearch.ping()
        if ping:
            logger.debug('elasticsearch connected')
            break
        else:
            logger.debug('elasticsearch not connected')
            await asyncio.sleep(2)
    
    app.ctx.users_repository = UsersRepositoryElasticsearch(app.ctx.elasticsearch)
    app.ctx.jokes_repository = JokesRepositoryElasticsearch(app.ctx.elasticsearch)
    
    app.ctx.client_session = aiohttp.ClientSession(raise_for_status=True)
    


@app.after_server_stop
async def teardown(app, loop):
    logger.debug('app.after_server_stop')
    await app.ctx.elasticsearch.close()
    await app.ctx.client_session.close()


@app.on_request
async def on_request(request):
    logger.debug('app.on_request')


@app.on_response
async def on_response(request, response):
    logger.debug('app.on_response')
    # logger.debug(request.headers)
    # logger.debug(response.headers)


@app.on_response
async def set_secure_headers(request, response):
    secure_headers.framework.sanic(response)
    logger.info(str(response.headers))


@app.on_response
async def add_request_id_header(request, response):
    response.headers["X-Request-ID"] = request.id

