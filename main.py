from enum import Enum
import random
import time

from player import *
from other import *


def main():

    # Pre Game
    turn = 0
    point_pool = POINTS[NUM_PLAYERS]

    cards = init_cards()

    players = [Player(i) for i in range(NUM_PLAYERS)]
    for _ in range(NUM_PLAYERS):
        player = Player(cards)
        player.setup()

    # Game Loop
    while True:
        print("Turn {}".format(turn))
        # If pool is empty, play until last player
        if point_pool <= 0 and turn % len(players) == 0:
            break

        cur_player = players[turn % len(players)]
        if not cur_player.spoiled:
            cur_player.plant()
        if not cur_player.spoiled:
            cur_player.harvest()
        cur_player.discard()
        cur_player.setup()

        import sys
        sys.stdout.flush()

        print()
        turn += 1

        time.sleep(0.5)

    # Post Game
    tally()

if __name__ == '__main__':
    main()
