from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, LinkPreviewOptions

from keyboards.train import get_yes_no_kb

router = Router()  # [1]


@router.message(Command('help', prefix='!'))
async def cmd_start(message: Message):
        text = ('🇺🇸 \n'
                'This bot is used to provide tekken frame data. \n'
                '!fd <character> <move> to get frame data needed.\n'
                '!characters to get full list of characters. \n'
                '!feedback to submit reports or give a feedback.\n'
                'Thank you!\n'
                'Please notice that this is an alpha version.\n'
                'Notation guide by Phidx: https://youtu.be/D58LncnVbXM?si=4a9uxS9R9Y8afXUs&t=22'
                '\n'
                '\n'
                '🇷🇺 \n'
                'Бот используется для получения фреймдаты для игры Tekken 8. \n'
                '!fd <персонаж> <мув> для получения фреймдаты. \n'
                '!characters для получения полного списка персонажей. \n'
                '!feedback - для отзыва любого характера. \n'
                'Спасибо! \n'
                'Пожалуйста учтите, что бот находится на альфа стадии. \n'
                'Гайд по нотации от BekaFGC: https://youtu.be/6A4-DS_Jol8?si=_tCeyE_ge4MYzp44&t=228'
                )
        await message.answer(text, link_preview_options=LinkPreviewOptions(is_disabled=True))


@router.message(Command('start'))
async def cmd_start(message: Message):
        text = ('This bot is used to provide tekken frame data. \n'
                'Please use !fd <character> <move> to get frame data needed.\n'
                'Use !characters to get full list of characters. \n'
                'Submit reports or feedback via !feedback.\n'
                'Thank you!\n'
                'Please notice that this is an alpha version.\n'
                'Notation guide by Phidx: https://youtu.be/D58LncnVbXM?si=4a9uxS9R9Y8afXUs&t=22'
                '\n'
                '\n'
                'Бот используется для получения фреймдаты для игры Tekken 8. \n'
                '!fd <персонаж> <мув> для получения фреймдаты. \n'
                '!characters для получения полного списка персонажей. \n'
                '!feedback - для отзыва любого характера. \n'
                'Спасибо! \n'
                'Пожалуйста учтите, что бот находится на альфа стадии. \n'
                'Гайд по нотации от BekaFGC: https://youtu.be/6A4-DS_Jol8?si=_tCeyE_ge4MYzp44&t=228'
                )
        await message.answer(text, link_preview_options=LinkPreviewOptions(is_disabled=True))