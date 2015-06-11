# encoding: utf-8
import random
from gibberish import Mirror

class Mosaic(object):

    @classmethod
    def from_template(self, template):
        pass

    def _cell(self, base, probabilities):
        for k, v in probabilities.items():
            if random.random() < v:
                return k
        return base

    def __init__(self):
        self.cells = []

    def populate(self, height, width, wmt, symmetrical_wmt=None, 
                 last_row_symmetrical=False,
                 last_column_symmetrical=False):
        self.cells = []
        for i in range(height):
            self.cells.append("")
            for j in range(width):
                symmetrical = (
                    (j == width-1 and last_column_symmetrical)
                    or (i == height-1 and last_row_symmetrical))
                if symmetrical and symmetrical_wmt:
                    table = symmetrical_wmt
                else:
                    table = wmt
                self.cells[-1] = self.cells[-1] + table.choice()

    @property
    def width(self):
        return len(self.cells[0])

    @property
    def height(self):
        return len(self.cells)

    def __unicode__(self):
        return "\n".join(self.cells)

    def mirror_horizontal(self, mirror_characters=True):
        """Return a new Mosaic that has this mosaic on the left and its mirror
        image to the right.
        """
        
        if self.width % 2 == 1:
            mirrored_width = self.width - 1
        else:
            mirrored_width = self.width

        mirror = Mosaic()
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
        mirror = Mosaic()
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

from pdb import set_trace
from randomness import WanderingMonsterTable
from gibberish import Alphabet


def make():
    alphabet = random.choice(Alphabet.TILABLE_CHARSET_S)
    if isinstance(alphabet, basestring):
        a = alphabet
        try:
            a = Alphabet.characters(a)
        except Exception, e:
            pass
    else:
        a = "".join(alphabet)
    # print a
    common = random.choice(a)
    if random.random() < 0.8:
        common += u" "
    wmt = WanderingMonsterTable(common, random.choice(a), random.choice(a))
    symmetricals = [x for x in a if not x in Mirror.horizontal
                    and not a in Mirror.vertical]
    sample_size = min(2, len(symmetricals))
    if not sample_size:
        symmetrical_wmt = None
        symm_hor = False
        symm_ver = False
    else:
        symmetrical_wmt = WanderingMonsterTable(
            random.sample(symmetricals, sample_size))
        #print "Symmetricals:"
        #for i in symmetricals:
        #    print i
        symm_hor = True
        symm_ver = True

    a = Mosaic()
    a.populate(6, 5, wmt, symmetrical_wmt, symm_hor, symm_ver)
    # print unicode(a)
    # print
    # print unicode(a.mirror_horizontal())

    # print
    # print unicode(a.mirror_vertical())

    # print
    print unicode(a.mirror_vertical(True).mirror_horizontal(True))

for alphabet in Alphabet.TILABLE_CHARSET_S:
    if isinstance(alphabet, basestring):
        try:
            alphabet = Alphabet.characters(alphabet)
        except KeyError, e:
            pass
        if len(alphabet) > 50:
            continue
        for i in alphabet:
            if i not in Mirror.left_right and i not in Mirror.top_bottom:
                print i
        print


for i in range(4):
    make()
    print
