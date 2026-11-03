class ItemClassification():
    filler = 0b00000
    """ aka trash, as in filler items like ammo, currency etc """

    progression = 0b00001
    """ Item that is logically relevant.
    Protects this item from being placed on excluded or unreachable locations. """

    useful = 0b00010
    """ Item that is especially useful.
    Protects this item from being placed on excluded or unreachable locations.
    When combined with another flag like "progression", it means "an especially useful progression item". """

    trap = 0b00100
    """ Item that is detrimental in some way. """

    skip_balancing = 0b01000
    """ should technically never occur on its own
    Item that is logically relevant, but progression balancing should not touch.

    Possible reasons for why an item should not be pulled ahead by progression balancing:
    1. This item is quite insignificant, so pulling it earlier doesn't help (currency/etc.)
    2. It is important for the player experience that this item is evenly distributed in the seed (e.g. goal items) """

    deprioritized = 0b10000
    """ Should technically never occur on its own.
    Will not be considered for priority locations,
    unless Priority Locations Fill runs out of regular progression items before filling all priority locations.

    Should be used for items that would feel bad for the player to find on a priority location.
    Usually, these are items that are plentiful or insignificant. """

    progression_deprioritized_skip_balancing = 0b11001
    """ Since a common case of both skip_balancing and deprioritized is "insignificant progression",
    these items often want both flags. """

    progression_skip_balancing = 0b01001  # only progression gets balanced
    progression_deprioritized = 0b10001  # only progression can be placed during priority fill