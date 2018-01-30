def seedling(player, card):
    card.reds = min(1, card.reds)

def per_helmets(resource, n=1):
    def inner(player, card):
        new_val = card.helmets * n + getattr(card, resource)
        setattr(card, resource, new_val)
    return inner

def centaur(player, card):
    player.extra_turn = True
    player.ppt += 2

def outcast(player, card):
    # TODO
    pass

def unicorn(player, card):
    # TODO
    pass

def make_token_active(player, card):
    # TODO Maybe ask player if they want to turn over token
    player.token_active = True

def discard_from_field(n=1):
    def inner(player, card):
        # TODO
        pass
    return inner

def wolf_rider(player, card):
    player.mana += max(0, 7 - len(player.field))

def discard_from_deck(n=1):
    def inner(player, card):
        # TODO
        pass
    return inner

def argent_owl(player, card):
    pass

def pridelord(player, card):
    if card.helmets >= 3:
        # More correct to set adv pts but shrug
        card.points += 4

def canopy_explorer(player, card):
    pass

def nightvale_pathfinder(player, card):
    pass

def peacekeeper_druid(player, card):
    pass

def beastbrother_hunter(player, card):
    player.ppt += max(0, 7 - len(player.field))

def burrow_wyrm(player, card):
    pass

def wind_whisperer(player, card):
    num_spr = card.b_spr + card.y_spr + card.g_spr
    card.b_spr, card.y_spr, card.g_spr = (0, 0, 0)
    card.w_spr += num_spr

def magpie(player, card):
    pass

def grovetender(player, card):
    card.green += card.helmets

def moss_troll(player, card):
    pass

def lifetap_oracle(player, card):
    pass

def ent_guard(player, card):
    for adv in card:
        if adv.rank == 1:
            card.helmets += 1

def hatchery(player, card):
    pass

def vale_bearer(player, card):
    if card.helemts >= 3:
        card.g_spr += 1
        card.y_spr += 1
        card.b_spr += 1

def overflow(player, card):
    player.mana *= 2

def call_of_the_hunt(player, card):
    while player.field < 8:
        player.draw(can_spoil=False)

def gaias_kin(player, card):
    pass

def stag_champion(player, card):
    card.ppt *= 2

def cancel_red(player, card):
    card.red = 0

def magic_seed(player, card):
    player.mana += len(player.field)

def calm_weather(player, card):
    pass

def primal_power(player, card):
    pass

def seed_sowers(player, card):
    pass

def sporeling_reclaimer(player, card):
    pass

def aurora(player, card):
    self.ppt += len(player.field) // 2

def gaias_chosen(player, card):
    pass

def dawnfire_dragon(player, card):
    pass


CARD_EFFECTS = {
    'Seedling': seedling,
    'Nymph': per_helmets('g_spr'),
    'Centaur': centaur,
    "Gaia's Outcast'": outcast,
    'Unicorn': unicorn,
    'Magic Mushroom': make_token_active,
    'Deadwood Harvester': discard_from_field(1),
    'Wolf Rider': wolf_rider,
    'Totem Chief': per_helmets('y_spr'),
    'Cleansing Rain': discard_from_deck(1),
    'Pack Leader': per_helmets('b_spr'),
    'Argent Owl': argent_owl,
    'Pridelord': pridelord,
    'Canopy Explorer': canopy_explorer,
    'Nightvale Pathfinder': nightvale_pathfinder,
    'Peacekeeper Druid': peacekeeper_druid,
    'Dawnsinger': per_helmets('mana'),
    'Mindfull Owl': discard_from_field(1),
    'Burrow Wyrm': burrow_wyrm,
    'Wind Whisperer': wind_whisperer,
    'Magpie': magpie,
    'Goldenwing Gryphon': make_token_active,
    'Grovetender': grovetender,
    'Beastbrother Hunter': beastbrother_hunter,
    'Moss Troll': moss_troll,
    'Lifetap Oracle': lifetap_oracle,
    'Ent Guard': ent_guard,
    'Feral Chieftain': per_helmets('ppt'),
    'Hatchery': hatchery,
    'Vale Bearer': vale_bearer,
    'Ley Line Overflow': overflow,
    'Lifebringer Seed': cancel_red,
    'Call of the Hunt': call_of_the_hunt,
    "Gaia's Kin": gaias_kin,
    'Woodland Warren': per_helmets('ppt', 2),
    'Stag Champion': stag_champion,
    'Magic Seed': magic_seed,
    'Calm Weather': calm_weather,
    'Primal Power': primal_power,
    'Seed Sowers': seed_sowers,
    'Sporeling Reclaimer': sporeling_reclaimer,
    'Aurora': aurora,
    "Gaia's Chosen": gaias_chosen,
    'Dawnfire Dragon': dawnfire_dragon,
}
