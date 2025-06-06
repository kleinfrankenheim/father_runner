import enum
import json
import re
from typing import List, Dict, Callable


class CharacterName(enum.Enum):
    ALISA = 'alisa'
    ASUKA = 'asuka'
    AZUCENA = 'azucena'
    BRYAN = 'bryan'
    CLAUDIO = 'claudio'
    CLIVE = 'clive'
    DEVIL_JIN = 'devil_jin'
    DRAGUNOV = 'dragunov'
    EDDY = 'eddy'
    FENG = 'feng'
    HEIHACHI = 'heihachi'
    HWOARANG = 'hwoarang'
    JACK_8 = 'jack_8'
    JIN = 'jin'
    JUN = 'jun'
    KAZUYA = 'kazuya'
    KING = 'king'
    KUMA = 'kuma'
    LARS = 'lars'
    LAW = 'law'
    LEE = 'lee'
    LEO = 'leo'
    LEROY = 'leroy'
    LIDIA = 'lidia'
    LILI = 'lili'
    NINA = 'nina'
    PANDA = 'panda'
    PAUL = 'paul'
    RAVEN = 'raven'
    REINA = 'reina'
    SHAHEEN = 'shaheen'
    STEVE = 'steve'
    VICTOR = 'victor'
    XIAOYU = 'xiaoyu'
    YOSHIMITSU = 'yoshimitsu'
    ZAFINA = 'zafina'


Character_alias = {
    CharacterName.ALISA: [],
    CharacterName.ASUKA: [],
    CharacterName.AZUCENA: ['azu', 'azuc', 'cafe'],
    CharacterName.BRYAN: ['byron', 'bry', 'bestchar'],
    CharacterName.CLAUDIO: ['serafino'],
    CharacterName.CLIVE: ['rosfield'],
    CharacterName.DEVIL_JIN: ['deviljin', 'dvj', 'dj', 'djin'],
    CharacterName.DRAGUNOV: ['drag', 'draga', 'sergei'],
    CharacterName.EDDY: ['capoeira'],
    CharacterName.FENG: ['fengwei'],
    CharacterName.HEIHACHI: ['heihach', 'hachi'],
    CharacterName.HWOARANG: ['hwo'],
    CharacterName.JACK_8: ['jack', 'jack8', 'j8'],
    CharacterName.JIN: ['jim'],
    CharacterName.JUN: ['junkazama'],
    CharacterName.KAZUYA: ['kazuya', 'kaz'],
    CharacterName.KING: ['jaguar', 'jaguarhead', 'cat'],
    CharacterName.KUMA: [],
    CharacterName.LARS: ['alexanderson'],
    CharacterName.LAW: ['law', 'marshall', 'ihaterichpeople'],
    CharacterName.LEE: ['excellent'],
    CharacterName.LEO: [],
    CharacterName.LEROY: ['leroysmith', 'smith', 'lsmith'],
    CharacterName.LIDIA: ['fftwo', 'lid', 'minister', 'pm'],
    CharacterName.LILI: [],
    CharacterName.NINA: [],
    CharacterName.PANDA: [],
    CharacterName.PAUL: [],
    CharacterName.RAVEN: ['crow'],
    CharacterName.REINA: [],
    CharacterName.SHAHEEN: [],
    CharacterName.STEVE: ['fox', 'stevefox', 'stv'],
    CharacterName.VICTOR: ['explosion', 'expulsion', 'vic'],
    CharacterName.YOSHIMITSU: ['yoshi', 'yosh'],
    CharacterName.XIAOYU: ['xiao', 'ling']

}

INPUT_FILTER = {
    ',': '',
    '/': '',
    r'd\+': 'd',
    r'f\+|F\+': 'f',
    r'b\+': 'b',
    r'df\+': 'df',
    r'uf\+': 'uf',
    r'ub\+': 'ub',
    r'db\+': 'db',
    r'cd\+': 'cd',
    r'wr\+': 'wr',
    r'fff': 'wr',
    r'\(': '',
    r'\)': '',
    r'\.': '',
    r'cd': 'fnddf'
}

MOVES_FILTER = {
    r'SLS': 'qcf'
}


# Function to filter inputs
def filter_input(input_foo):
    for key_foo, value_foo in INPUT_FILTER.items():
        input_foo = re.sub(key_foo, value_foo, input_foo, flags=re.I)

    for key_foo1, value_foo1 in MOVES_FILTER.items():
        input_foo = re.sub(key_foo1, value_foo1, input_foo, flags=re.I)

    return input_foo.lower()


def compare_inputs(data, command_input):
    found_move = ''
    found_input = filter_input(command_input)

    counter = 0
    # Iterating through every dict while changing the command key values and comparing them to input
    for any_move in data:
        found_move = filter_input(any_move['command'])
        # print(any_move['command'])

        # only comparing when the whole input filter is finished
        if found_input != found_move:
            counter = 0

        elif found_input == found_move:
            return any_move

    return None


def get_character_by_name(user_input):
    result = None

    for any_character in CharacterName:
        if user_input.lower() == any_character.value:
            result = any_character.value
            return result

    # any_key corresponds to keys of Character_alias dictionary
    # any_value list corresponds to a list of the dictionary
    # matched any_key value is returned, if user_input matches any of the aliases from any list
    if result is None:
        for any_key, any_value_list in Character_alias.items():
            if user_input.lower() in any_value_list:
                result = any_key.value
                return result

    return None


'''
# Used for debugging purposes
user_input = "kaz"
character = get_character_by_name(user_input)

if character:
    print(f"Matched character: {character}")
else:
    print(f"'{user_input}' is not a valid character.")

print(compare_inputs())
'''
