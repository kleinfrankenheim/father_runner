import re

from aiogram import Router, F
from aiogram.types import Message

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
    checked_user = await middleware_instance.SetObject.check_user(user_id=message.reply_to_message.from_user.id)

    user_firstname = message.reply_to_message.from_user.first_name
    if checked_user:
        await message.reply(text=f'Я уважаю пользователя {user_firstname}')
    elif not checked_user:
        await message.reply(text=f'Я игнорирую пользователя: {user_firstname}')


@router.message()
async def answer_to_him(message: Message):

    try:
        response = await create_response(message.text)
    except Exception as e:
        await message.reply(text=f'Ошибка: {e}')
    else:
        await message.reply(response)
