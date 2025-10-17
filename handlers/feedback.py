import os

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from dotenv import load_dotenv

load_dotenv()

feedback_chat_id = int(os.getenv('FEEDBACK_CHAT_ID'))

router = Router()


class GivingFeedback(StatesGroup):
    waiting_for_feedback = State()


@router.message(Command('feedback', prefix='!'))
async def feedback_template(message: Message, state: FSMContext):
    await message.answer('Please provide information about any bugs you have discovered\n'
                         '<Character>\n'
                         '<Move\n'
                         '<Exactly how you typed your message>\n'
                         'Thank you!')

    # Setting the state 'waiting for feedback'
    await state.set_state(GivingFeedback.waiting_for_feedback)


@router.message(GivingFeedback.waiting_for_feedback)
async def handling_feedback(message: Message, state: FSMContext):
    await message.reply('Thanks for your feedback!')

    await message.bot.send_message(chat_id=feedback_chat_id, text=message.text + '\n' + message.from_user.username)
    await state.clear()
