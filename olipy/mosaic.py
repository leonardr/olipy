# encoding: utf-8
from pdb import set_trace
import re
import random
from olipy.randomness import WanderingMonsterTable
from olipy.gibberish import Alphabet, MosaicGibberish

class Mosaic(object):

    @classmethod
    def from_template(self, template, mapping):
        pass

    def __init__(self):
        self.cells = []

    @property
    def width(self):
        return len(self.cells[0])

    @property
    def height(self):
        return len(self.cells)

    def __unicode__(self):
        return "\n".join(self.cells)

class SymmetryList(object):

    def __init__(self, alphabet):
        self.horizontal = [x for x in alphabet if not x in Mirror.horizontal]
        self.vertical = [x for x in alphabet if not x in Mirror.horizontal]
        self.full = [x for x in self.horizontal if x in self.vertical]

    def choice(self, fallback, horizontal=True, vertical=True):
        x = None
        if horizontal and vertical:
            x = self.full
        elif horizontal:
            x = self.horizontal
        elif vertical:
            x = self.vertical
        if x:
            return random.choice(x)
        else:
            return fallback.choice()
        

class SymmetricalMosaic(Mosaic):

    def __init__(self, wmt=None, symmetry_list=None):
        self.wmt = wmt
        self.symmetry_list = symmetry_list
        super(SymmetricalMosaic, self).__init__()

    @classmethod
    def from_alphabet(cls, alphabet, common_spaces=False):
        wmt, symmetry_list = cls.make_wmt(alphabet, common_spaces)        
        return SymmetricalMosaic(wmt, symmetry_list)

    @classmethod
    def make_wmt(cls, alphabet, num_spaces=0):
        if isinstance(alphabet, list) or isinstance(alphabet, tuple):
            alphabet = "".join(alphabet)
        try:
            alphabet = Alphabet.characters(alphabet)
        except KeyError as e:
            pass
        common = uncommon = rare = None

        if len(alphabet) == 1:
            if not num_spaces:
                raise ValueError("Can't make a mosaic from a single character")
            common = alphabet
        elif len(alphabet) == 2:
            common = alphabet
        else:
            common, uncommon, rare = random.sample(alphabet, 3)
        common += u"\N{EM SPACE}" * num_spaces
        return (WanderingMonsterTable(common, uncommon, rare),
                SymmetryList(alphabet))

    @classmethod
    def random_size(cls, max_size=140, horizontal_symmetry=False,
                    vertical_symmetry=False):
        max_width = 14
        if horizontal_symmetry:
            max_width /= 2
        width = random.randint(3, int(max_width))

        max_height = min(10, max_size/(width+1))
        if vertical_symmetry:
            max_height /= 2
        height = random.randint(3, int(max_height))
        return height, width

    def populate(self, height, width, horizontal_symmetry=False,
                 vertical_symmetry=False):
        self.cells = []
        for i in range(height):
            self.cells.append("")
            for j in range(width):
                need_vertical_symmetry = (
                    j == width-1 and vertical_symmetry)
                need_horizontal_symmetry = (
                    i == height-1 and horizontal_symmetry)
                self.cells[-1] += self.choice(
                    need_horizontal_symmetry, need_vertical_symmetry)
        m = self
        if horizontal_symmetry:
            m = m.mirror_horizontal()
        if vertical_symmetry:
            m = m.mirror_vertical()
        return m

    def choice(self, need_horizontal_symmetry, need_vertical_symmetry):
        return self.symmetry_list.choice(
            self.wmt, need_horizontal_symmetry, need_vertical_symmetry)

    def mirror_horizontal(self, mirror_characters=True):
        """Return a new Mosaic that has this mosaic on the left and its mirror
        image to the right.
        """
        
        if self.width % 2 == 1:
            mirrored_width = self.width - 1
        else:
            mirrored_width = self.width

        mirror = SymmetricalMosaic()
        for row in self.cells:
            new_part = row[:mirrored_width][::-1]
            if mirror_characters:
                new_part = self.mirror_string_horizontal(new_part)
            mirror.cells.append(row + new_part)
        return mirror

    def mirror_vertical(self, mirror_characters=True):
        """Return a new Mosaic that has this mosaic on the top and its mirror
        image beneath.
        """
        mirror = SymmetricalMosaic()
        for row in self.cells:
            mirror.cells.append(row)
        for row in self.cells[:-1][::-1]:
            new_row = row
            if mirror_characters:
                new_row = self.mirror_string_vertical(new_row)
            mirror.cells.append(new_row)
        return mirror

    def mirror_string_horizontal(self, s):
        new_string = ''
        for i in s:
            if i in Mirror.horizontal:
                new_string += Mirror.horizontal[i]
            else:
                new_string += i
        return new_string

    def mirror_string_vertical(self, s):
        new_string = ''
        for i in s:
            if i in Mirror.vertical:
                new_string += Mirror.vertical[i]
            else:
                new_string += i
        return new_string

class MirroredMosaicGibberish(MosaicGibberish):

    def __init__(self, alphabet=None):
        if not alphabet:
            if random.randint(0, 5) == 2:
                # Give emoji a boost
                alphabet = "Emoji"
            else:
                alphabet = random.choice(Alphabet.TILABLE_CHARSET_S)
        self.alphabet = alphabet

    def tweet(self):
        a = random.random()
        hor_sym = False
        ver_sym = False
        if a < 0.25:
            hor_sym = True
        elif a < 0.4:
            ver_sym = True
        elif a < 0.95:
            hor_sym = ver_sym = True

        mostly_space = False
        if random.random() < 0.6:
            # Primarily characters.
            num_spaces = int(random.gauss(1.3,1))
        else:
            # Primarily whitespace
            num_spaces = random.randint(len(self.alphabet), len(self.alphabet)*2)
            mostly_space = True
        height, width = SymmetricalMosaic.random_size(140, hor_sym, ver_sym)

        mosaic = SymmetricalMosaic.from_alphabet(self.alphabet, num_spaces)
        m = mosaic.populate(height, width, hor_sym, ver_sym)
        m = m.__unicode__()
        if not m[0].strip():
            # This tweet starts with whitespace. Use COMBINING
            # GRAPHEME JOINER to get Twitter to preserve the whitespace.
            #
            # TODO: It's not clear whether this works.
            m = u"\N{COMBINING GRAPHEME JOINER}" + m
        return m

class Mirror(object):
    """Information about which characters mirror to which other characters."""

    left_right = u"""
◐◑
▌▐
╭╮
╰╯
└┘
┗┙
┖┚
┗┛
┌┐
┍┑
┎┒
┏┓
├┤
┝┥
┞┦
┟┧
┠┨
┡┩
┢┪
┽┾
╃╄
╅╆
╉╊
╸╺
╼╾
╱╲
▖▗
▜▛
▙▟
▘▝
▚▞
⬔◩
⬕◪
◧◨
▧▨
╒╕
╓╖
╔╗
╘╛
╙╜
╚╝
╞╡
╟╢
╠╣
╶╴
┣┫
┹┺
┵┶
┱┲
┭┮
╒╕
╓╖
╔╗
╘╛
╙╜
╚╝
"""

    top_bottom = u"""
    ╰╭
    ╯╮
    ╱╲
    ╀╁
    ╇╈
    ╹╻
    ╽╿
    ▀▄
    ◒◓
    ▚▞
    ▜▟
    ▙▛
    ⬔◪
    ⬕◩
    ⬒⬓
    ▧▨
┴┬
╘╒
╚╔
╝╗
╧╤
╙╖
╨╥
╛╕
╜╓
╩╦
╵╷
┳┻
╹╻
╽╿
╦╩
╥╨
╧╤
╩╦
╘╒
╙╓
╚╔
╛╕
╜╖
╝╗
    """



    def _make_mirror(s):
        m = {}
        parts = re.compile("\s+").split(s)
        for p in parts:
            p = p.strip()
            if not p:
                continue
            a, b = p
            m[a] = b
            m[b] = a
        return m

    horizontal = _make_mirror(left_right)
    vertical = _make_mirror(top_bottom)

    @classmethod
    def potentials(classmethod):
        """Report on characters that might need to be added to this class."""
        for alphabet in Alphabet.TILABLE_CHARSET_S:
            if isinstance(alphabet, basestring):
                try:
                    alphabet = Alphabet.characters(alphabet)
                except KeyError as e:
                    pass
                if len(alphabet) > 50:
                    continue
                for i in alphabet:
                    if i not in cls.left_right and i not in cls.top_bottom:
                        print(i)
                    print("\n")

if __name__ == '__main__':
    for i in range(4):
        print(MirroredMosaicGibberish().tweet())
        print("\n")
