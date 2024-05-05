from aiogram.filters import BaseFilter
from aiogram.types import Message
from data.get_id import user_id_in_table

class IsRegisteredUser(BaseFilter):
    async def __call__(self, message: Message):
        user_id = message.from_user.id
        if await user_id_in_table(user_id):
            return True
        return False