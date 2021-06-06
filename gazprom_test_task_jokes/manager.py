from sanic import Blueprint
from sanic import HTTPResponse
from sanic import json
from sanic import Request
from sanic import Sanic
from sanic_cors import CORS
# noinspection PyUnresolvedReferences
from sanic_jwt_extended import JWT
from sanic_limiter import get_remote_address
from sanic_limiter import Limiter
from sanic_openapi import swagger_blueprint
from sanic_sslify import SSLify
from sanic_testing import TestManager
from secure import secure

app = Sanic(__name__)
TestManager(app)


CORS(app)
# SanicUserAgent.init_app(app)
sslify = SSLify(app)
secure_headers = secure.Secure()
app.blueprint(swagger_blueprint)

with JWT.initialize(app) as manager:
    manager.config.secret_key = "secret"
    manager.config.use_blacklist = True

app.config.SWAGGER_UI_CONFIGURATION = {
    'validatorUrl':           app.config.SWAGGER_UI_CONFIGURATION_VALIDATOR_URL,
    'displayRequestDuration': app.config.SWAGGER_UI_CONFIGURATION_DISPLAY_REQUEST_DURATION,
    'docExpansion':           app.config.SWAGGER_UI_CONFIGURATION_DOC_EXPANSION,
    }

limiter = Limiter(
    app,
    global_limits=[
        app.config.LIMITER_PER_HOUR,
        app.config.LIMITER_PER_SECOND,
        ],
    key_func=get_remote_address,
    strategy='moving-window',
    storage_uri="memory://"
    )
