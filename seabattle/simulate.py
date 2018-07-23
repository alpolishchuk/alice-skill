# coding: utf-8
import sys
import importlib
import logging


logging.basicConfig(format='%(message)s', level=logging.INFO)


player_1 = importlib.import_module(sys.argv[1])
player_2 = importlib.import_module(sys.argv[2])

game_1 = player_1.Game()
game_2 = player_2.Game()

game_1.start_new_game()
game_2.start_new_game()

print 'Player 1 field:'
game_1.print_field()
print 'Player 2 field:'
game_2.print_field()


def get_name(game):
    if game is game_1:
        return 'Player 1'
    else:
        return 'Player 2'


def prepare_text_coords(coords):
    return coords.replace(',', '')


active = game_1
passive = game_2


# MAIN LOOP
while True:
    coords = active.convert_to_position(prepare_text_coords(active.do_shot()))
    print '{}: MOVE {}-{}'.format(get_name(active), coords[0], coords[1])
    result = passive.handle_enemy_shot(coords)
    print '{}: {}'.format(get_name(passive), result.upper())
    active.handle_enemy_reply(result)

    if result == 'miss':
        active, passive = passive, active

    should_exit = False

    if game_1.is_victory():
        print 'Player 1: VICTORY'
        should_exit = True
    elif game_1.is_defeat():
        print 'Player 1: DEFEAT'
        should_exit = True

    if game_2.is_victory():
        print 'Player 2: VICTORY'
        should_exit = True
    elif game_2.is_defeat():
        print 'Player 2: DEFEAT'
        should_exit = True

    if should_exit:
        break


print '=' * 50
print 'Player 1 field:'
print 'His POV:'
game_1.print_field()
print 'Opponents POV:'
game_2.print_enemy_field()

print 'Player 2 field:'
print 'His POV:'
game_2.print_field()
print 'Opponents POV:'
game_1.print_enemy_field()
