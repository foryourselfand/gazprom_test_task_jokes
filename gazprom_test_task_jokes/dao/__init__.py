from gazprom_test_task_jokes.model.user import User


class UserDAO(User):

    @classmethod
    async def get_user(cls, user_id):
        user = await cls.get_or_404(user_id)
        return user
