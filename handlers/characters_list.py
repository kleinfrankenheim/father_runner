from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

router = Router()  # [1]


@router.message(Command('characters', prefix='!'))
async def characters_list(message: Message):
    text = (f'`Alisa` \n'
            f'`Anna` \n'
            f'`ArmorKing` \n'
            f'`Asuka` \n'
            f'`Azucena` \n'
            f'`Bryan` \n'
            f'`Claudio` \n'
            f'`Clive` \n'
            f'`Devil\\_jin` \n'
            f'`Dragunov` \n'
            f'`Eddy` \n'
            f'`Feng` \n'
            f'`Heihachi` \n'
            f'`Hwoarang` \n'
            f'`Jack\\_8` \n'
            f'`Jin` \n'
            f'`Jun` \n'
            f'`Kazuya` \n'
            f'`King` \n'
            f'`Kuma` \n'
            f'`Lars` \n'
            f'`Law` \n'
            f'`Lee` \n'
            f'`Leo` \n'
            f'`Leroy` \n'
            f'`Lidia` \n'
            f'`Lili` \n'
            f'`Nina` \n'
            f'`Panda` \n'
            f'`Paul` \n'
            f'`Raven` \n'
            f'`Reina` \n'
            f'`Shaheen` \n'
            f'`Steve` \n'
            f'`Victor` \n'
            f'`Xiaoyu` \n'
            f'`Yoshimitsu` \n'
            f'`Zafina` \n'
            f'*Every name can be copied \n'
            f'Just click on it*')
    await message.answer(text, parse_mode=ParseMode.MARKDOWN_V2)