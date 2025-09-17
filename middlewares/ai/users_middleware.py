import os
import re
import asyncio

from typing import Callable, Dict, Awaitable, Any, List, Set
from aiogram import BaseMiddleware, F

from aiogram.types import Message

admin_id = int(os.getenv('ADMIN_ID'))

permission_text = 'Нет привелегий.'
error_text = 'Что-то пошло не так.'
success_text = 'Успешно.'


def error_message():
    return permission_text


class FilterException(Exception):
    default_message = 'Нет привелегий'

    def __init__(self, message: str = None):
        message = message if message is not None else self.default_message
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class PermissionException(FilterException):
    default_message = 'Нет привелегий.'


class UserAlreadyExistsException(FilterException):
    default_message = 'Пользователь уже имеет права.'


class UserNotFoundException(FilterException):
    default_message = 'Пользователь не имеет прав.'



# Actually a class to filter out people who can use AI.
# Admin should be able to add and remove users from the set.
class FilterClass:

    def __init__(self) -> None:
        self.allowed_set: Set = {admin_id}
        self.admin_id: int = admin_id
        self.lock = asyncio.Lock()

    def is_admin(self, user_id: int) -> bool:
        return user_id == self.admin_id

    async def check_user(self, user_id) -> Any:
        async with self.lock:
            return user_id in self.allowed_set

    async def add_user(self, caller_id: int, new_user_id: int) -> Any:

        async with self.lock:
            if not self.is_admin(caller_id):
                raise PermissionException
            if new_user_id in self.allowed_set:
                raise UserAlreadyExistsException

            self.allowed_set.add(new_user_id)
            return success_text

    async def remove_user(self, caller_id: int, new_user_id: int) -> Any:

        async with self.lock:
            if not self.is_admin(caller_id):
                raise PermissionException
            if new_user_id not in self.allowed_set:
                raise UserNotFoundException

            self.allowed_set.remove(new_user_id)
            return success_text

    def get_set(self) -> Set:

        return self.allowed_set


# Middleware itself. Testing
class AIFilterMiddleware(BaseMiddleware):

    def __init__(self) -> None:
        super().__init__()
        self.SetObject = FilterClass()

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],

    ) -> Any:
        user_id = event.from_user.id
        message_text = event.text

        match_check = (re.match(pattern='фазерраннер|fatherrunner', string=message_text, flags=re.I))

        if (user_id in self.SetObject.get_set()) and match_check:
            return await handler(event, data)
        return None
