import re

from aiogram.filters.base import Filter
from aiogram.types import Message


# class checks if user input matches with the given string
# Firstly was used for Fatherrunner commands (check usages)
# Now it will be used for general input checking
# TODO: Comment this section better.

class GeneralInputMatchCheck(Filter):

    def __init__(self, check_text: str) -> None:

        pattern_foo = rf'^{check_text}$'

        self.check_text = check_text
        self.pattern = re.compile(pattern_foo, re.I)

    async def __call__(self, message: Message) -> bool:

        check_text = message.text.strip()
        print(check_text)

        return True if self.pattern.match(message.text) else False
