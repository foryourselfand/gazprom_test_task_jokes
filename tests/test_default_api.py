from sanic import Sanic
from sanic.response import json
from sanic_testing import TestManager
import pytest


@pytest.fixture
def app():
    sanic_app = Sanic(__name__)
    TestManager(sanic_app)

    @sanic_app.get("/")
    def basic(request):
        return json({"message": "hello Sanic!"})

    return sanic_app


@pytest.mark.asyncio
async def test_sanic_default_api(app):
    request, response = await app.asgi_client.get("/")

    assert response.status == 200
    assert response.json == {"message": "hello Sanic!"}


# async def test_sanic_default_api(app):
#     response = await app.get("/")
#     assert response.status == 200
