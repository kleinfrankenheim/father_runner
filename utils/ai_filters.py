import re

from aiogram.filters.base import Filter
from aiogram.types import Message


class AuthorizationFilter(Filter):

    def __init__(self, check_text: str) -> None:
        self.check_text = check_text

    async def __call__(self, message: Message) -> bool:
        result = re.match(pattern=self.check_text,
                          string=message.text,
                          flags=re.I)

        return True if result else None



