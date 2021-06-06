import pytest
from sanic import Blueprint
from sanic import Sanic

from route.health import health


@pytest.fixture
def app():
    sanic_app = Sanic(__name__)
    
    api = Blueprint.group(health, url_prefix="/api", version=1)
    sanic_app.blueprint(api)
    
    return sanic_app


@pytest.mark.asyncio
async def test_health_api(app):
    request, response = await app.asgi_client.get("/v1/api/health/status")
    
    assert response.status == 200
    assert response.json['status'] == "OK"
