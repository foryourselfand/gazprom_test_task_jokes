from sanic import Sanic
from sanic_limiter import get_remote_address, Limiter


def configure_swagger_ui(app: Sanic) -> None:
    app.config.SWAGGER_UI_CONFIGURATION = {
        'validatorUrl':           None,
        'displayRequestDuration': True,
        'docExpansion':           'full'
        }


def setup_rate_limiter(app: Sanic) -> Limiter:
    return Limiter(
        app,
        global_limits=[
            "1000/hour",
            "100/second"
            ],
        key_func=get_remote_address,
        strategy='moving-window',
        storage_uri="memory://")
