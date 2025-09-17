import enum
import json
import re
from typing import List, Dict, Callable


class CharacterName(enum.Enum):
    ANNA = 'anna'
    ALISA = 'alisa'
    ASUKA = 'asuka'
    AZUCENA = 'azucena'
    BRYAN = 'bryan'
    CLAUDIO = 'claudio'
    CLIVE = 'clive'
    DEVIL_JIN = 'devil_jin'
    DRAGUNOV = 'dragunov'
    EDDY = 'eddy'
    FAHKUMRAM = 'fahkumram'
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
    CharacterName.ANNA: [],
    CharacterName.ASUKA: ['oscar'],
    CharacterName.AZUCENA: ['azu', 'azuc', 'cafe'],
    CharacterName.BRYAN: ['byron', 'bry', 'bestchar'],
    CharacterName.CLAUDIO: ['serafino'],
    CharacterName.CLIVE: ['rosfield'],
    CharacterName.DEVIL_JIN: ['deviljin', 'dvj', 'dj', 'djin'],
    CharacterName.DRAGUNOV: ['drag', 'draga', 'sergei'],
    CharacterName.EDDY: ['capoeira'],
    CharacterName.FAHKUMRAM: ['fahk', 'fakhumram', 'fakh'],
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
    'bryan': [r'qcf', 'sls', r'qcb', 'hatchet'],
    'heihachi': [r'ewgf', 'fnddf:2'],
    'jin': [r'zen', 'b3+4', r'ewhf', 'fnddfdf:2', r'ewgf', 'fnddfdf:2'],
    'kazuya': [r'ewgf', 'fnddf:2'],
    'lidia': ['hea', 'hae'],
    'lili': [r'qcf', 'dew'],
    'paul': [r'deathfist', 'qcf2'],
    'reina': [r'ewgf', 'fnddf:2'],
    'steve': [r'alb', '3+4'],
    'yoshimitsu': [r'flash', '1+4'],

}


# Function to open files
def open_frame_data(file_path):
    with open(file_path) as file:
        data = json.load(file)

        return data


# Function to filter inputs
def filter_input(input_foo):
    for key_foo, value_foo in INPUT_FILTER.items():
        input_foo = re.sub(key_foo, value_foo, input_foo, flags=re.I)

    return input_foo.lower()


# Function to filter to treat movement inputs as stance moves names/
# For example:
# BRYAN - SLS should be treated as qcf.
# If user inputs (!fd bryan qcf1+2) it should give SLS.1+2 instead. Because they are basically the same.
# MOVES_FILTER is a dictionary that built like this: { characters: [(SLS), (qcf1+2)] }
# The odd number of the list(SLS) is the input that needs to be changed and the even number is the input that should be
# treated(qcf). SLS>qcf.

def filter_moves(input_foo, character_foo):
    counter = 1
    odd_list = []
    even_list = []

    # Iterating through main dictionary.
    for ch_move_pair in MOVES_FILTER.items():
        counter = 1
        character = ch_move_pair[0]
        moves = ch_move_pair[1]
        if character == character_foo:

            # Creating 2 lists:
            # First one is for odd (check 125-126 lines).
            # Second one is for even.
            for move in moves:
                if counter % 2 == 1:
                    odd_list.append(move)
                elif counter % 2 == 0:
                    even_list.append(move)
                counter = counter + 1

            # Now we should create a dictionary which should just look like INPUT_FILTER
            # {(string that needs to be changed): (the string that needs to be changed into)}
            filter_dict = dict(zip(odd_list, even_list))

            for key_foo, value_foo in filter_dict.items():
                input_foo = re.sub(key_foo, value_foo, input_foo, flags=re.I)

    return input_foo


def compare_inputs(data_given, character_name, command_input):
    found_move = ''
    found_input = filter_input(command_input)
    found_input = filter_moves(found_input, character_foo=character_name)

    counter = 0
    # Iterating through every dict while changing the command key values and comparing them to input
    for any_move in data_given:
        found_move = filter_input(any_move['command'])
        found_move = filter_moves(input_foo=found_move, character_foo=character_name)
        # print(any_move['command'])

        # only comparing when the whole input filter is finished
        if found_input != found_move:
            counter = 0

        elif found_input == found_move:
            return any_move

    return None


def get_character_by_name(character_input):
    result = None

    for any_character in CharacterName:
        if character_input.lower() == any_character.value:
            result = any_character.value
            return result

    # any_key corresponds to keys of Character_alias dictionary
    # any_value list corresponds to a list of the dictionary
    # matched any_key value is returned, if user_input matches any of the aliases from any list
    if result is None:
        for any_key, any_value_list in Character_alias.items():
            if character_input.lower() in any_value_list:
                result = any_key.value
                return result

    return None

# # Used for debugging purposes
# user_input = "kaz"
# filtered_input = filter_input('qcf1+2')
# character_name_gotten = get_character_by_name('byron')
# print(filter_moves('sls1+2', 'bryan'))
#
# data = open_frame_data('./output/bryan.json')
# printable_junk = compare_inputs(data, character_name_gotten, 'qcf1+2')
#
# print(printable_junk)

# text_try = '!fd dvj 1+2'.split()[1]
# print(text_try)
# getchar = get_character_by_name(text_try)
# print(getchar)

# data = open_frame_data('./output/jin.json')
# printable_junk = compare_inputs(data, 'jin', 'f3+4,2')
# print(printable_junk)