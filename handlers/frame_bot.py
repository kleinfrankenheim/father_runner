import json
from aiogram import Router, F
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message
from aiogram.filters import Command

from replace_train import get_character_by_name, compare_inputs

router = Router()


# Function to find move needed
def open_frame_data(file_path):
    with open(file_path) as file:
        data = json.load(file)

        return data


@router.message(F.text.startswith('!fd '))
async def answer_frame(message: Message):
    found_move = {}
    notes = ''
    found_notes = ''
    character = message.text.split()[1]
    move = message.text.split()[2]

    # character = character.lower()
    character = get_character_by_name(character)
    path = './output/' + character + '.json'

    returned_data = open_frame_data(path)

    compare_inputs(returned_data, move)
    found_move = compare_inputs(returned_data, move)
    try:
        notes = found_move['notes'].split('*')
    except TypeError:
        await message.reply(f'Couldnt find the move you were looking for\n'
                            f'Submit feedback via !feedback if needed')

    for note in notes:
        found_notes = found_notes + '🗒 ' + note + '\n'

    await message.reply(f'🤹🏻 Character: {character.capitalize()}\n'
                        f'🦾 command: {found_move['command']}\n'
                        f'🤜🏿 hit level: {found_move['hit level']}\n'
                        f'1️⃣ damage: {found_move['damage']}\n'
                        f'ℹ️ startup: {found_move['startup']}\n'
                        f'🟦 on block: {found_move['block']}\n'
                        f'🟥 on hit: {found_move['hit']}\n'
                        f'⚡️ on counter hit: {found_move['counter hit']}\n'
                        f'📌 Notes: {found_notes}')
