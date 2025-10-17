

from aiogram import Router
from aiogram.types import Message, FSInputFile

from utils.general import GeneralInputMatchCheck

router = Router()

itak_checker = GeneralInputMatchCheck('итак')

photo_file_id = ''
photo_from_system = FSInputFile(path="./images/itak.png")

@router.message(itak_checker)
async def itak_respond(message: Message):
    await message.answer_photo(photo='AgACAgIAAyEGAASpnvKrAAMKaPKcKsBZKd3hL0I1Hfmetzk6LdIAArz7MRuPWJlLYq9lWf1vpZEBAAMCAAN4AAM2BA')