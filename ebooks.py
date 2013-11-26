import random
import textwrap

class EbooksQuotes(object):

    def __init__(self, keywords=None, probability=0.001, 
                 maximum_quote_size=140, wrap_at=23,
                 truncate_chance=1.0/4):
        keywords = keywords or []
        self.keywords = [x.lower() for x in keywords]
        self.probability = probability
        self.maximum_quote_size = maximum_quote_size
        self.wrap_at = wrap_at
        self.truncate_chance = truncate_chance

    def quotes_in(self, paragraph):
        para = textwrap.wrap(paragraph, self.wrap_at)
        gathering = False
        in_progress = None
        for i in range(len(para)):
            line = para[i]
            if gathering:
                # We are currently putting together a quote.
                yielding = False
                if random.random() < self.truncate_chance:
                    # Yield a truncated quote.
                    yielding = True
                else:
                    potential = in_progress + ' ' + line.strip()
                    if len(potential) >= self.maximum_quote_size:
                        # That would be too long. We're done.
                        yielding = True
                    else:
                        in_progress = potential

                if yielding:
                    yield in_progress
                    in_progress = None
                    gathering = yielding = False

            else:
                # We are not currently gathering a quote. Should we
                # be?
                matches = self._line_matches(line)
                if matches or random.random() < self.probability:
                    gathering = True
                    if matches:
                        # A keyword match! Start gathering a quote either
                        # at this line or some earlier line.
                        maximum_backtrack = (self.maximum_quote_size / self.wrap_at) - 1
                        backtrack = random.randint(0, maximum_backtrack)

                        start_at = max(0, i - backtrack)
                        in_progress = " ".join(
                            [x.strip() for x in para[start_at:i+1]])
                    else:
                        in_progress = line.strip()
                    

    def _line_matches(self, line):
        l = line.lower()
        for keyword in self.keywords:
            if keyword in l:
                return True
        return False

