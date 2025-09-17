from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()  # [1]


@router.message(Command('help', prefix='!'))
async def cmd_start(message: Message):
    await message.answer(
        'This bot is used to provide tekken frame data. \n'
        'Please use !fd <character> <move> to get frame data needed.\n'
        'Submit reports or feedback via !feedback.\n'
        'Thank you!\n'
        'Please notice that this is an alpha version.',
    )
