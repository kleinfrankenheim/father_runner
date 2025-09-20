import re

from aiogram import Router, F
from aiogram.types import Message

# Database module import
from database.models.models import AllowedUsersDocument

# AI module Imports
from middlewares.ai.users_middleware import AIFilterMiddleware, PermissionException
from utils.ai_filters import AuthorizationFilter
from utils.openai_util import create_response

router = Router()

# Instance created to access the list of users.
# Using AIFilterMiddleware messes up the process of adding, removing new users.
middleware_instance = AIFilterMiddleware()

router.message.middleware(middleware_instance)


@router.message(AuthorizationFilter('Фазерраннер добавь'))
async def user_add(message: Message):
    try:
        await message.reply(await middleware_instance.SetObject.add_user(caller_id=message.from_user.id,
                                                                         new_user_id=message.reply_to_message.from_user.id))

    except Exception as e:

        await message.reply(e.__str__())


@router.message(AuthorizationFilter('Фазерраннер удали'))
async def user_remove(message: Message):
    try:
        await message.reply(await middleware_instance.SetObject.remove_user(caller_id=message.from_user.id,
                                                                            new_user_id=message.reply_to_message.from_user.id))
    except Exception as e:
        await message.reply(e.__str__())


@router.message(AuthorizationFilter('Фазерраннер проверь'))
async def user_check(message: Message):
    # Has been modified so user can check if he can talk to the bot or not.

    reply_user_exists = False
    reply_user_firstname = 0
    reply_user_id = 0

    # 1. Turns out Python by default throws AttributeError when (if message.reply_to_message.from_user.id is not None).
    #   Python checks attribute access before it checks for (is not None), so if message.reply_to_message turns out to
    #   be None: it cant get None.from_user or even more None.from_user.id and it it throws AttributeError. Because
    #   of that every attribute needs to be checked (or at least that is what I found to be the solution)

    # 1. Checks if reply message exists.
    # 2. If reply message exists > reply_user_firstname and reply_user_id are taken from replied message.
    # 3. If otherwise reply_user_firstname and reply_user_id are taken from user that calls the command.
    if (
            message.reply_to_message is not None
            and message.reply_to_message.from_user is not None
            and message.reply_to_message.from_user.id is not None
    ):
        reply_user_exists = True
    else:
        reply_user_exists = False

    if reply_user_exists:
        reply_user_firstname = message.reply_to_message.from_user.first_name
        reply_user_id = message.reply_to_message.from_user.id
    elif not reply_user_exists:
        reply_user_firstname = message.from_user.first_name
        reply_user_id = message.from_user.id

    checked_user = await middleware_instance.SetObject.check_user(user_id=reply_user_id)

    if checked_user:
        await message.reply(text=f'Я уважаю пользователя {reply_user_firstname}')
    elif not checked_user:
        await message.reply(text=f'Я игнорирую пользователя: {reply_user_firstname}')


@router.message()
async def answer_to_him(message: Message):
    try:
        response = await create_response(message.text)
    except Exception as e:
        await message.reply(text=f'Ошибка: {e}')
    else:
        await message.reply(response)
