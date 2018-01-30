from enum import Enum
import random
import time

from other import *

NUM_DECK = 20
NUM_BLANKS = 8
MAX_EFF_REDS = 3
class Player():
    def __init__(self, purchase_field, pool, i: int):
        # Accumulate total for each phase, so effects can take place
        # on the totals
        self.purchase_field = purchase_field
        self.pool = pool
        self.num = i

        cursed_lands = [ Card(base=Advancement("Cursed Land", pos, 0, 0, mana=1, red=1),
                              perm_pos=pos)
                         for pos in NORM_POS ] * 3
        fertile_soils = [ Card(base=Advancement("Fertile Soil", pos, 0, 0, mana=1),
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

        # assert(0 <= self.mana)
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
        assert(len(self.field) == 0)

        # Get redness of previous card
        if self.on_deck:
            self.red = self.on_deck.get_red()
            self.green = self.on_deck.get_green()

        # Draw cards
        while self.eff_red() < MAX_EFF_REDS and (len(self.deck) + len(self.discards)) > 0:
            self.draw()

        if MAX_EFF_REDS < self.eff_red():
            self.spoiled = True
            return

    def draw(self, can_spoil=True):
        assert(len(self.deck) > 0 or len(self.discards))
        if self.on_deck is None:
            self.deck += self.discards
            self.discards = []
            random.shuffle(self.deck)
            self.on_deck = self.deck.pop(0)
        else:
            self.field.append(self.on_deck)
            self.apply(lambda adv: adv.played_f, self.on_deck)
            if len(self.deck) == 0:
                self.deck += self.discards
                random.shuffle(self.deck)
                self.discards = []
            self.on_deck = self.deck.pop(0)

        self.red += self.on_deck.get_red()
        self.green += self.on_deck.get_green()

    @assert_invariants
    def plant(self):
        push = False

        if push:
            # Draw cards
            if len(self.deck) + len(self.discard) > 0:
                self.draw()

            if MAX_EFF_REDS < self.eff_red:
                self.spoiled = True
                return

    @assert_invariants
    def harvest(self):

        # Harvest Priority 5 - Sum up base stuff
        for card in self.field:
            self.mana += card.get_mana()
            self.ppt += card.get_ppt()


        print("PPT: {}".format(self.ppt))
        print("Eff Red: {}".format(self.eff_red()))
        print(self.field, self.on_deck)

        # Simple Buying AI
        done = False
        for i, adv in list(enumerate(self.purchase_field.purchasable()))[::-1]:
            if self.mana >= adv.cost:
                for card in self.field:
                    if adv.pos not in card.filled_slots():
                        self.mana -= adv.cost
                        self.purchase_field.purchase(i)
                        card.purchases.append(adv)
                        done = True
                        break
                if done:
                    break

        # Take points from pool
        self.points += self.pool.take(self.ppt)

    @assert_invariants
    def discard(self):
        # Apply purchased advancements
        for card in self.field:
            card.apply_purchases()

        # TODO Apply fancy effects

        self.discards += self.field
        self.field = []

    def end_game(self):
        for card in self.field:
            self.points += card.get_points()

    def spoil(self):
        self.spoiled = False

        self.token_active = True
