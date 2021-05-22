from gazprom_test_task_jokes.dao import UserDAO

from sanic import Blueprint
from sanic.response import json


user = Blueprint(name="user", url_prefix="/user")

@user.route("/<user_id:int>")
async def get_user(request, user_id):
    user = await UserDAO.get_user(user_id)
    return json(user.to_dict())
