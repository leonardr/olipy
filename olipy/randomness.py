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

    def _bucket_for(self, freq):
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
        return l

    def add(self, o, freq):
        self._bucket_for(freq).append(o)

    def choice(self, freq=None):
        if freq is not None:
            l = self._bucket_for(freq)
        else:
            c = random.randint(0, 99)
            if c < 65:
                l = self.common
            elif c < 85:
                l = self.uncommon
            elif c < 96:
                l = self.rare
            else:
                l = self.very_rare
            if not l:
                l = self.common
        return random.choice(l)

class Gradient(object):

    @classmethod
    def gradient(cls, go_from, go_to, length):
        """Yields a gradient from set1 to set2 of a given length."""
        for i in range(int(length)):
            chance = float(i)/length
            if random.random() > chance:
                c = go_from
            else:
                c = go_to
            yield random.choice(c)

    @classmethod
    def rainbow_gradient(cls, go_from, go_to, length):
        "Goes from go_from to go_to and back again."
        l1 = length / 2
        l2 = length - l1
        for x in cls.gradient(go_from, go_to, l1):
            yield x
        for x in cls.gradient(go_to, go_from, l2):
            yield x
