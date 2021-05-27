from gazprom_test_task_jokes.gazprom_test_task_jokes import app
from gazprom_test_task_jokes.util import sanic_config_manager

sanic_config_manager(app, prefix="SANIC_")

if __name__ == "__main__":
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        workers=app.config['WORKERS'],
        debug=app.config['DEBUG'] == 'True',
        access_log=app.config['ACCESS_LOG'] == 'True',
        )
