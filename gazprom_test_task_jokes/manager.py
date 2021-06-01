from sanic import Sanic
from sanic_cors import CORS
# noinspection PyUnresolvedReferences
from sanic_jwt_extended import JWT
from sanic_limiter import get_remote_address, Limiter
from sanic_openapi import swagger_blueprint
from sanic_sslify import SSLify
from sanic_useragent import SanicUserAgent
from secure import secure


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


app = Sanic(__name__)

CORS(app)
configure_swagger_ui(app)
SanicUserAgent.init_app(app)
sslify = SSLify(app)
limiter = setup_rate_limiter(app)
secure_headers = secure.Secure()
app.blueprint(swagger_blueprint)

with JWT.initialize(app) as manager:
    manager.config.secret_key = "secret"
    manager.config.use_blacklist = True
