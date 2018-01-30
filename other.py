from enum import Enum
import random
import time

from player import *

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
        self.perm_pos = perm_pos
        self.purchases = []

        self.recompute()
        self.compute()

    def compute(self):
        # TODO Handle ongoing and such
        if not self.computed:
            for adv in self:
                self.helmets += adv.helmets
                self.mana += adv.mana
                self.ppt += adv.ppt
                self.g_spr += adv.g_spr
                self.y_spr += adv.y_spr
                self.b_spr += adv.b_spr
                self.w_spr += adv.w_spr
                self.red += adv.red
                self.green += adv.green

            self.computed = True

    def recompute(self):
        self.helmets = 0
        self.mana = 0
        self.ppt = 0
        self.g_spr = 0
        self.y_spr = 0
        self.b_spr = 0
        self.w_spr = 0
        self.red = 0
        self.green = 0

        self.computed = False

    def apply_purchases(self):
        for purchase in self.purchases:
            self.adv.append(purchase)
            self.recompute()

    def get_red(self):
        # TODO Handle ongoing effects
        self.compute()
        return self.red

    def get_eff_red(self):
        self.compute()
        return self.red

    def get_green(self):
        self.compute()
        return self.green

    def get_mana(self):
        self.compute()
        return self.mana

    def get_g_spr(self):
        self.compute()
        return self.g_spr

    def get_y_spr(self):
        self.compute()
        return self.y_spr

    def get_b_spr(self):
        self.compute()
        return self.b_spr

    def get_w_spr(self):
        self.compute()
        return self.w_spr

    def get_ppt(self):
        self.compute()
        return self.ppt

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

