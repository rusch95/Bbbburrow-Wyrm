from enum import Enum
import random
import time

from player import *
from other import *


def main():

    # Pre Game
    turn = 0

    point_pool = PointPool(POINTS[NUM_PLAYERS])
    purchase_field = init_cards()

    players = [Player(purchase_field, point_pool, i) for i in range(NUM_PLAYERS)]
    for player in players:
        player.setup()

    # Game Loop
    while True:
        print("Player {} Turn {}".format((turn % NUM_PLAYERS + 1), (turn // NUM_PLAYERS + 1)))
        # If pool is empty, play until last player
        if point_pool.n <= 0 and turn % len(players) == 0:
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

    # Post Game
    for player in players:
        print("Player {} has {} points".format(player.num, player.points))

if __name__ == '__main__':
    main()
