# encoding: utf-8
from olipy.randomness import WanderingMonsterTable
import random

class Typewriter(object):
    """Simulates the Adler Universal 39 typewriter used in "The Shining"
    and the sorts of typos that are commonly made on that typewriter.

    Originally written for @a_dull_bot.
    """
    neighbors = dict(
        A = "SQZW",
        l = "kop:,.",
        w = "q23esa",
        o = "90ipkl:",
        r = "45etdfg",
        k = "iojlm,",
        a = "sqzw",
        n = "bjkm ",
        d = "ersfxc",
        p = u"0-=o½l:",
        y = "67tughj",
        m = "jkln, ",
        e = "34wrsdf",
        s = "weadzx",
        J = "YUIHKNM",
        c = "dfxv ",
        u = "78yihj",
        b = "ghvn ",
    )
    neighbors[" "] = "    zxcvbnm,./"
    neighbors["."] = "l;,/"

    def __init__(b, mean_transforms=1.4, stdev_transforms=0.5):
        """Simulate someone hacking away at a typewriter

        :param mean_transforms: The mean number of mistakes per 100
        characters.

        :param stdev_stransforms: The acceptable standard
        deviation from the mean.
        """
        b.mean_transforms = mean_transforms
        b.stdev_transforms = stdev_transforms
        b.wmt = WanderingMonsterTable(
            common=[
                b.typo, b.typo, b.duplicate, b.transpose
            ],
            uncommon=[b.omit_period, b.delete_space, b.typo_add, b.delete],
            rare=[b.delete, b.lowercase_uppercase_letter,
                  b.extra_space_at_beginning, b.uppercase_letter],
            very_rare=[b.uppercase_word, b.uppercase_entire_string,
                       b.lowercase_entire_string, b.remove_word,
                       b.delete],
        )


    def find_typo(self, correct):
        if correct not in self.neighbors:
            # This is already a typo.
            return correct
        return random.choice(self.neighbors[correct])

    def typo(self, string):
        # Replace one character with a typo.
        if not string:
            return string
        i = random.randint(0, len(string)-1)
        incorrect = self.find_typo(string[i])
        return string[:i] + incorrect + string[i+1:]

    def typo_add(self, string):
        # Add a typo character hit before or after the correct character.
        if not string:
            return string
        i = random.randint(0, len(string)-1)
        correct = string[i]
        incorrect = self.find_typo(correct)
        if random.random() < 0.5:
            incorrect = correct + incorrect
        else:
            incorrect = incorrect + correct
        return string[:i] + incorrect + string[i+1:]

    def transpose(self, string):
        # Transpose two characters.
        if len(string) < 2:
            return string
        i = random.randint(0, len(string)-2)
        return string[:i] + string[i+1] + string[i] + string[i+2:]

    def duplicate(self, string):
        # Duplicate a character.
        if not string:
            return string
        i = random.randint(0, len(string)-1)
        return string[:i] + string[i] + string[i] + string[i+1:]

    def delete(self, string):
        # Delete a character.
        if not string:
            return string
        i = random.randint(0, len(string)-1)
        return string[:i] + string[i+1:]

    def delete_space(self, string):
        poses = [i for i, c in enumerate(string) if c == ' ']
        if not poses:
            return string
        i = random.choice(poses)
        return string[:i] + string[i+1:]

    def uppercase_word(self, string):
        words = string.split(" ")
        if not words:
            return string
        i = random.randint(0, len(words)-1)
        return " ".join(words[:i] + [words[i].upper()] + words[i+1:])

    def lowercase_uppercase_letter(self, string):
        poses = [(i,c) for i, c in enumerate(string) if c.upper() == c]
        i,c = random.choice(poses)
        return string[:i] + c.lower() + string[i+1:]

    def uppercase_letter(self, string):
        if not string:
            return string
        i = random.randint(0, len(string)-1)
        return string[:i] + string[i].upper() + string[i+1:]

    def uppercase_entire_string(self, string):
        return string.upper()

    def lowercase_entire_string(self, string):
        return string.upper()
    
    def remove_word(self, string):
        words = string.split(" ")
        if not words:
            return string
        i = random.randint(0, len(words)-1)
        return " ".join(words[:i] + words[i+1:])

    def omit_period(self, string):
        if not string:
            return string
        if string[-1] == '.':
            return string[:-1]
        return string

    def extra_space_at_beginning(self, string):
        return u"\N{EN SPACE}" + string

    def type(self, correct, so_far=""):
        length = len(correct)
        s = str(correct)
        transforms_per_100 = random.gauss(
            self.mean_transforms, self.stdev_transforms
        )
        chunks_100 = max(1, length/100)
        total_transforms = max(1, transforms_per_100 * chunks_100)

        for i in range(int(total_transforms)):
            s = self.wmt.choice()(s)
        s = so_far + s
        if random.random() < 0.1 and len(s) < 100:
            # If it's short, we may type the whole thing again.
            s = self.type(correct, s + " ")
        return s
