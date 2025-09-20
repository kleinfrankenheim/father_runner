import os
import re
import asyncio

from typing import Callable, Dict, Awaitable, Any, List, Set
from aiogram import BaseMiddleware, F
from aiogram.types import Message

from database.models.models import AllowedUsersDocument, AllowedUsersDocumentView

admin_id: int = int(os.getenv('ADMIN_ID'))

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

    # 1.Function that connects to the database MongoDB database,
    #   takes all the documents from ai_allowed_users doc collections. Check models in database.models.models.py .
    # 2. Then it creates a set from all 'tg_id' field.
    # 3. Concatenates the set with admin_id and returns.
    # 4. At the same time it updates self.allowed_set everytime it gets called.
    # 5. get_full_set gets called everytime before new_user being added or existing user being deleted.
    async def get_full_set(self):
        docs = await AllowedUsersDocument.find().project(AllowedUsersDocumentView).to_list()
        set_from_docs = {doc.tg_id for doc in docs}
        full_set_with_admin = self.allowed_set.union(set_from_docs)
        self.allowed_set = full_set_with_admin

        return full_set_with_admin

    # Checks if user exists in allowed list.
    async def check_user(self, user_id) -> Any:
        async with self.lock:
            await self.get_full_set()
            return user_id in self.allowed_set

    async def add_user(self, caller_id: int, new_user_id: int) -> Any:

        await self.get_full_set()

        async with self.lock:

            # Only admin can add new_users and line #87 makes sure that user doesn't already exist.
            if not self.is_admin(caller_id):
                raise PermissionException
            if new_user_id in self.allowed_set:
                raise UserAlreadyExistsException

            new_user_doc = AllowedUsersDocument(tg_id=new_user_id)
            await new_user_doc.insert()
            self.allowed_set.add(new_user_id)
            return success_text

    async def remove_user(self, caller_id: int, new_user_id: int) -> Any:

        await self.get_full_set()

        # Only admin can delete users and line #103 makes sure that user does exist in the list in the first place.
        async with self.lock:
            if not self.is_admin(caller_id):
                raise PermissionException
            if new_user_id not in self.allowed_set:
                raise UserNotFoundException

            await AllowedUsersDocument.find(AllowedUsersDocument.tg_id == new_user_id).delete()
            self.allowed_set.remove(new_user_id)
            return success_text


# Middleware itself.
# 1. To pass through this middleware users message needs to start with 'фазерраннер' or 'fatherrunner'.
#   User also should be in the allowed set. Check the lines 127-137.
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

        full_set_with_admin = await self.SetObject.get_full_set()

        if (user_id in full_set_with_admin) and match_check:
            return await handler(event, data)
        return None
