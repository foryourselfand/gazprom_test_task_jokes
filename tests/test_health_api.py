from sanic import Sanic
from sanic_testing import TestManager
from sanic.response import json
import pytest


@pytest.fixture
def app():
    sanic_app = Sanic(__name__)
    TestManager(sanic_app)

    @sanic_app.get("/health/status")
    def get_health_status(request):
        return json({"status": "OK"})

    return sanic_app


@pytest.mark.asyncio
async def test_sanic_default_api(app):
    request, response = await app.asgi_client.get("/health/status")

    assert response.status == 200
    assert response.json == {"status": "OK"}


# async def test_sanic_default_api(sanic_tester: SanicTestClient):
#     response = await sanic_tester.get("/health/status")
#     assert response.status == 200
#     json_response = await response.json()
#     assert json_response["status"] == "OK"


