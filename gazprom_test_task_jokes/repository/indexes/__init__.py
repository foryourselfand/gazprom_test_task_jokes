from sanic import text
from sanic.log import logger
from sanic_openapi.openapi2 import doc

from manager import app


@app.route('/index_users_create_', methods=['GET'])
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


@app.route('/index_jokes_create', methods=['GET'])
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
                "joke":     {
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
