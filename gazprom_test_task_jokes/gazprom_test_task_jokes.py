from elasticsearch import AsyncElasticsearch
from sanic import Blueprint, text
from sanic.log import logger
from sanic_openapi.openapi2 import doc

from blueprint.auth import auth
from blueprint.jokes import jokes
from manager import app, secure_headers

api = Blueprint.group(auth, jokes, url_prefix="/api", version=1)
app.blueprint(api)


@app.before_server_start
async def setup(app, loop):
    logger.debug('app.before_server_start')
    app.ctx.elasticsearch = AsyncElasticsearch([{
        'host': app.config.ELASTICSEARCH_HOST,
        'port': app.config.ELASTICSEARCH_PORT
        }])
    ping = await app.ctx.elasticsearch.ping()
    if ping:
        logger.debug('elasticsearch connected')
    else:
        logger.debug('elasticsearch not connected')


@app.after_server_stop
async def teardown(app, loop):
    logger.debug('app.after_server_stop')
    await app.ctx.elasticsearch.close()


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


@app.route('/create_users_index', methods=['GET'])
@doc.route(exclude=True)
async def create_users_index(request):
    index_name = 'users'
    settings = {
        "settings": {
            "number_of_shards":   5,
            "number_of_replicas": 1
            },
        "mappings": {
            "dynamic":    "strict",
            "properties": {
                "username": {
                    "type": "text"
                    },
                "password": {
                    "type": "text"
                    },
                }
            }
        }
    
    created = False
    try:
        exist = await app.ctx.elasticsearch.indices.exists(index_name)
        if not exist:
            created = await app.ctx.elasticsearch.indices.create(index=index_name, body=settings)
    except Exception as e:
        logger.debug(e)
    
    if created:
        return text(f'{index_name} index created')
    else:
        return text(f'{index_name} index not created')


@app.route('/create_jokes_index', methods=['GET'])
@doc.route(exclude=True)
async def create_jokes_index(request):
    index_name = 'jokes'
    settings = {
        "settings": {
            "number_of_shards":   5,
            "number_of_replicas": 1
            },
        "mappings": {
            "dynamic":    "strict",
            "properties": {
                "username": {
                    "type": "text"
                    },
                "joke": {
                    "type": "text"
                    },
                }
            }
        }
    
    created = False
    try:
        exist = await app.ctx.elasticsearch.indices.exists(index_name)
        if not exist:
            created = await app.ctx.elasticsearch.indices.create(index=index_name, body=settings)
    except Exception as e:
        logger.debug(e)
    
    if created:
        return text(f'{index_name} index created')
    else:
        return text(f'{index_name} index not created')
