from sanic.log import logger
from sanic_fire import cmd
from sanic_fire.core import command_class, command_func

from gazprom_test_task_jokes import app


@command_class
class Hello(object):
    """ Annonation """

    def hello(self, value = 'world'):
        """ hello """
        return 'hello, ' + str(value)


@command_func
async def create_users_index():
    index_name = 'users'
    settings = {
        "settings": {
            "number_of_shards":   5,
            "number_of_replicas": 1
            },
        "mappings": {
            "dynamic":    "strict",
            "properties": {
                "name": {
                    "type": "text"
                    },
                }
            }
        }

    created = False
    try:
        exist = await app.ctx.elastic_search.indices.exists(index_name)
        logger.debug(exist)
        if not exist:
            created = await app.ctx.elastic_search.indices.create(index=index_name, body=settings)
    except Exception as e:
        logger.debug(e)

    if created:
        return f'{index_name} index created'
    else:
        return f'{index_name} index not created'


if __name__ == '__main__':
    cmd()
