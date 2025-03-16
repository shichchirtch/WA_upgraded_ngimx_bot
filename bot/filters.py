from aiogram.filters import BaseFilter
from aiogram.types import Message


class SHOW_BUTTON(BaseFilter):
    async def __call__(self, message: Message):
        if message.text == '* Show my Orders *':
            return True
        return False