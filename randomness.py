"""Sophisticated tools for random choices."""
import random

COMMON = "common"                 # 65%
UNCOMMON = "uncommon"             # 20%
RARE = "rare"                     # 11%
VERY_RARE = "very rare"           # 4%

class WanderingMonsterTable(object):
    """Uses 1st edition AD&D rules to weight a random choice.

    Any given choice may be COMMON, UNCOMMON, RARE, or VERY RARE.
    """

    def __init__(self, common=None, uncommon=None, rare=None,
                 very_rare=None):
        self.common = common or []
        self.uncommon = uncommon or []
        self.rare = rare or []
        self.very_rare = very_rare or []

    def add(self, o, freq):
        if freq == COMMON:
            l = self.common
        elif freq == UNCOMMON:
            l = self.uncommon
        elif freq == RARE:
            l = self.rare
        elif freq == VERY_RARE:
            l = self.very_rare
        else:
            raise ValueError("Invalid value for _freq: %s" % freq)
        l.append(o)

    def choice(self):
        c = random.randint(0, 99)
        if c < 65:
            l = self.common
        elif c < 85:
            l = self.uncommon
        elif c < 96:
            l = self.rare
        else:
            l = self.very_rare
        return random.choice(l)
