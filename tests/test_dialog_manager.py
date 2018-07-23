# coding: utf-8

from __future__ import unicode_literals

from seabattle import dialog_manager as dm, game as gm
from seabattle import session

import mock


user_id = 'user1'
session_obj = session.get(user_id)


def say(message):
    return dm.DialogManager(session_obj).handle_message(message).text


def newgame(opponent):
    return dm.MESSAGE_TEMPLATES['newgame'] % {'opponent': opponent}


def shot(shot):
    return dm.MESSAGE_TEMPLATES['shot'] % {'shot': shot}


def miss(shot):
    return dm.MESSAGE_TEMPLATES['miss'] % {'shot': shot}


def kill():
    return dm.MESSAGE_TEMPLATES['kill']


def hit():
    return dm.MESSAGE_TEMPLATES['hit']


def defeat():
    return dm.MESSAGE_TEMPLATES['defeat']


def opponent(name):
    return '%s, ' % name


def test_game_1():
    assert say('новая игра. соперник яндекс') == newgame('яндекс')

    field = [gm.EMPTY, gm.EMPTY, gm.EMPTY,
             gm.SHIP,  gm.EMPTY, gm.SHIP,
             gm.EMPTY, gm.EMPTY, gm.SHIP]

    my_field = [gm.EMPTY, gm.SHIP,  gm.EMPTY,
                gm.EMPTY, gm.EMPTY, gm.EMPTY,
                gm.EMPTY, gm.SHIP,  gm.SHIP]

    shots = ['1, 1', '1, 2', '2, 3', '3, 3', '1, 3']

    game = gm.Game()
    game.start_new_game(3, field, [2, 1])
    game.do_shot = mock.Mock(side_effect=shots)
    game.repeat = mock.Mock(return_value='2, 3')

    session_obj['game'] = game

    assert say('начинай') == opponent('яндекс') + shot(shots[0])
    assert say('мимо. я хожу 2 2') == miss(shots[1])
    assert say('мимо. я хожу 3 2') == hit()
    assert say('я хожу 3 3') == kill()
    assert say('я хожу 2 3') == miss(shots[2])
    assert say('я не понял') == opponent('яндекс') + miss('2, 3')
    assert say('ты попала') == shot(shots[3])
    assert say('корабль утонул') == shot(shots[4])
    assert say('мимо. я хожу 1 2') == kill()
    assert say('ура победа') == defeat()
