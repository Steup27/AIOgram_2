from random import choice
from database.database import data
from lexicon.lexicon import LEXICON_RU

def check_user(message):
    if message.from_user.id not in data:
        data[message.from_user.id] = {'name': message.from_user.first_name,
                                      'cnt': 0,
                                      'cnt_win': 0,
                                      'cnt_draw': 0}

def opponents_option(message):
    response_options = ['rock', 'scissors', 'paper']
    opponent = choice(response_options)
    return opponent

def get_result(message, opponent):
    pairs_options = {(LEXICON_RU['rock'], LEXICON_RU['rock']): "nobody_won",
                     (LEXICON_RU['rock'], LEXICON_RU['scissors']): "user_won",
                     (LEXICON_RU['rock'], LEXICON_RU['paper']): "bot_won",
                     (LEXICON_RU['scissors'], LEXICON_RU['rock']): "bot_won",
                     (LEXICON_RU['scissors'], LEXICON_RU['scissors']): "nobody_won",
                     (LEXICON_RU['scissors'], LEXICON_RU['paper']): "user_won",
                     (LEXICON_RU['paper'], LEXICON_RU['rock']): "user_won",
                     (LEXICON_RU['paper'], LEXICON_RU['scissors']): "bot_won",
                     (LEXICON_RU['paper'], LEXICON_RU['paper']): "nobody_won"
                     }
    pair = (message.text, LEXICON_RU[opponent])
    result = pairs_options[pair]
    data[message.from_user.id]['cnt'] += 1
    if result == "nobody_won":
        data[message.from_user.id]['cnt_draw'] += 1
    elif result == "user_won":
        data[message.from_user.id]['cnt_win'] += 1
    return result

def get_statistics(message):
    gamer = message.from_user.id
    all = data[gamer]['cnt']
    win = data[gamer]['cnt_win']
    draw = data[gamer]['cnt_draw']
    loss = all - win - draw
    return f'Количество побед: {win}\n'\
           f'Количество поражений: {loss}\n'\
           f'Количество ничейных результатов: {draw}\n'\
           f'Всего сыграно игр: {all}'

