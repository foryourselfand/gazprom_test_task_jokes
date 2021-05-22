from gazprom_test_task_jokes.gazprom_test_task_jokes import app
from gazprom_test_task_jokes.plugin.opentracing import setup_opentracing
from gazprom_test_task_jokes.util import sanic_config_manager

setup_opentracing(app=app)

sanic_config_manager(app, prefix="SANIC_")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8888,
        worker=4,
        )
