from enum import Enum
import random
import time


class Pos(Enum):
    none = 0
    top = 1
    mid = 2
    bot = 3
    topback = 4
    midback = 5
    botback = 6

NORM_POS = [Pos.top, Pos.mid, Pos.bot]


class Func():

    def __init__(self, f, priority):
        self.f = f
        self.p = priority  # Certain functions should go before other ones


class Advancement():

    def __init__ (
        self,
        name: str,
        pos: Pos,  # Position of the card
        cost: int,  # Cost in mana of the card
        rank: int,
        mana: int = 0,
        ppt: int = 0,  # Points per Turn
        points: int = 0,  # Points tallied at the end of the game
        g_spr: int = 0,  # Green Spirits
        y_spr: int = 0,  # Yellow Spirits
        b_spr: int = 0,  # Brown Spirits
        w_spr: int = 0,  # Wild Spirits
        helmets: int = 0,
        red: int = 0,  # Number of Red Trees
        green: int = 0,  # Number of Green Trees
        ongoing_f: Func = None,
        ondeck_f: Func = None,
        played_f: Func = None,
        plant_f: Func = None,
        harvest_f: Func = None,
        gather_f: Func = None,
        end_game_f: Func = None,
    ):

        self.name = name
        self.pos = pos
        self.cost = cost
        self.rank = rank
        self.mana = mana
        self.ppt = ppt
        self.points = points
        self.g_spr = g_spr
        self.y_spr = y_spr
        self.b_spr = b_spr
        self.w_spr = w_spr
        self.helmets = helmets
        self.red = red
        self.green = green
        self.ongoing_f = ongoing_f
        self.ondeck_f = ondeck_f
        self.played_f = played_f
        self.plant_f = plant_f
        self.harvest_f = harvest_f
        self.gather_f = gather_f
        self.end_game_f = end_game_f

        assert(0 <= cost <= 10)
        assert(0 <= rank <= 3)
        assert(0 <= mana)
        assert(0 <= ppt)
        assert(0 <= g_spr)
        assert(0 <= y_spr)
        assert(0 <= b_spr)
        assert(0 <= w_spr)
        assert(0 <= helmets)
        assert(0 <= red)
        assert(0 <= green)


class Card():
    def __init__(self, base=None, perm_pos: Pos = Pos.none):
        # Attrs that need to be glommed for effects
        if base:
            self.adv = [base]
        else:
            self.adv = []
        self.helmets = 0
        self.mana = 0
        self.ppt = 0
        self.g_spr = 0
        self.y_spr = 0
        self.b_spr = 0
        self.w_spr = 0
        self.red = 0
        self.green = 0
        self.perm_pos = perm_pos

    def get_red(self):
        # TODO Handle ongoing effects
        return self.red

    def get_eff_red(self):
        # TODO Handle ongoing effects
        return self.red

    def get_green(self):
        # TODO Handle ongoing effects
        return self.green

    def __iter__(self):
        return iter(self.adv)

    def __str__(self):
        # TODO Represent backing cards
        top, mid, bot = "None", "None", "None"
        for adv in self.adv:
            if Pos.top == adv.pos:
                top = adv.name
        for adv in self.adv:
            if Pos.mid == adv.pos:
                mid = adv.name
        for adv in self.adv:
            if Pos.bot == adv.pos:
                bot = adv.name

        return "[{}, {}, {}]".format(top, mid, bot)

    def __repr__(self):
        return self.__str__()

def assert_invariants(f):
    def inner(self, *args, **kwargs):
        self.invariants()
        f(self, *args, **kwargs)
        self.invariants()

    return inner


NUM_DECK = 20
NUM_BLANKS = 8
MAX_EFF_REDS = 3
class Player():
    def __init__(self, i: int):
        # Accumulate total for each phase, so effects can take place
        # on the totals
        self.num = i

        cursed_lands = [ Card(base=Advancement("Cursed Land", pos, 0, 1, red = 1),
                              perm_pos=pos)
                         for pos in NORM_POS ] * 3
        fertile_soils = [ Card(base=Advancement("Fertile Soil", pos, 0, 1),
                               perm_pos=pos)
                          for pos in NORM_POS ]
        blank_cards = [ Card() for _ in range(NUM_BLANKS) ]
        self.deck = cursed_lands + fertile_soils + blank_cards
        self.discards = []
        self.field = []
        self.on_deck = None

        self.points = 0
        self.token_active = False
        self.zero_acc()

    def apply(self, f_f, card):
        # f_f is a function that returns a function that does stuff
        for adv in card:
            f = f_f(adv)
            if f is not None:
                f(self, card)

    def invariants(self):
        assert(len(self.deck) + len(self.discards) + len(self.field) +
               (1 if self.on_deck is not None else 0) == NUM_DECK)
        assert(self.on_deck or self.on_deck is None)

        assert(0 <= self.mana)
        assert(0 <= self.g_spirits)
        assert(0 <= self.y_spirits)
        assert(0 <= self.b_spirits)
        assert(0 <= self.w_spirits)

        assert(0 <= self.red)
        assert(0 <= self.green)

    def eff_red(self):
        return self.red - self.green

    def zero_acc(self):
        # Set the various accumulators to zero
        self.ppt = 0  # Points per turn

        self.mana = 0
        self.g_spirits = 0
        self.y_spirits = 0
        self.b_spirits = 0
        self.w_spirits = 0

        self.red = 0
        self.green = 0

        self.spoiled = False

    @assert_invariants
    def setup(self):
        # Pre-Turn Stuff
        self.zero_acc()

        # Draw cards
        while self.eff_red() <= MAX_EFF_REDS and len(self.deck) > 0:
            self.draw()

        if MAX_EFF_REDS < self.eff_red():
            self.spoiled = True
            return

    def draw(self, can_spoil=True):
        assert(len(self.deck) > 0)
        if self.on_deck is None:
            self.deck += self.discards
            self.discards = []
            random.shuffle(self.deck)
            self.on_deck = self.deck.pop(0)
            print(self.on_deck)
            import sys
            sys.stdout.flush()

        else:
            self.field.append(self.on_deck)
            self.apply(lambda adv: adv.played_f, self.on_deck)
            self.on_deck = self.deck.pop(0)

        self.red += self.on_deck.get_red()
        self.green += self.on_deck.get_green()


    @assert_invariants
    def plant(self):
        push = False

        if push:
            # Draw cards
            if len(self.deck) > 0:
                self.draw()

            if MAX_EFF_REDS < self.eff_red:
                self.spoiled = True
                return


    @assert_invariants
    def harvest(self):
        pass

    @assert_invariants
    def discard(self):
        # Apply purchased advancements

        # TODO Apply fancy effects

        self.discards += self.field
        self.field = []

    def spoil(self):
        self.spoiled = False

        self.token_active = True

class PurchaseField():
    def __init__(self, thing):

        adv_ones = []
        adv_twos = []
        adv_threes = []
        vale_ones = []
        vale_twos = []

        # TODO Fertile Soils
        self.adv_ones = random.shuffle(adv_ones)
        self.adv_twos = random.shuffle(adv_twos)
        self.adv_threes = random.shuffle(adv_threes)
        self.vale_ones = random.shuffle(vale_ones)
        self.vale_twos = random.shuffle(vale_twos)

class PointPool():
    def __init__(self, size):
        self.size = size


def init_cards():

    purchase_field = PurchaseField(None)

    return purchase_field

def tally():
    pass

NUM_PLAYERS = 3
POINTS = [0, 18, 18, 23, 27, 31]  # TODO This is current wrong

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
        # If pool is empty, play until last player
        if point_pool <= 0 and turn % len(players) == 0:
            break

        cur_player = players[turn % len(players)]
        if not cur_player.spoil:
            cur_player.plant()
        if not cur_player.spoil:
            cur_player.harvest()
        cur_player.discard()
        cur_player.setup()

        turn += 1

    # Post Game
    tally()

if __name__ == '__main__':
    main()
