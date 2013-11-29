from random import choice

class MarkovGenerator(object):

    """A token generator using a Markov chain with configurable order.
    
    Queneau assembly is usually better than a Markov chain above the
    word level (constructing paragraphs from sentences) and below the word
    level (constructing words from phonemes), but Markov chains are
    usually better when assembling sequences of words.
    """

    def __init__(self, order=1, max=500):
        self.order = order # order (length) of ngrams
        self.max = max # maximum number of elements to generate
        self.ngrams = dict() # ngrams as keys; next elements as values
        self.beginnings = list() # beginning ngram of every line

    @classmethod
    def load(cls, f, order=1, max=500):
        """Load from a filehandle that defines a single chunk of text."""
        corpus = MarkovGenerator(n, max)
        corpus.add(f.read())
        return corpus

    @classmethod
    def loadlines(cls, f, order=1, max=500):
        """Load from a filehandle that defines one text per line."""
        corpus = MarkovGenerator(n, max)
        for l in f:
            corpus.add(l.strip())
        return corpus

    def tokenize(self, text):
        return text.split(" ")

    def add(self, text):
        tokens = self.tokenize(text)
        # discard this line if it's too short
        if len(tokens) < self.order:
            return

        # store the first ngram of this line
        beginning = tuple(tokens[:self.order])
        self.beginnings.append(beginning)

        i = 0
        for i in range(len(tokens) - self.order):

            gram = tuple(tokens[i:i+self.order])
            next = tokens[i+self.order] # get the element after the gram

            # if we've already seen this ngram, append; otherwise, set the
            # value for this key as a new list
            self.ngrams.setdefault(gram, []).append(next)

        if i > 0:
            # Store the fact that a given token was the last one on the line.
            final_gram = tuple(tokens[i+1:i+self.order+1])
            self.ngrams.setdefault(final_gram, []).append(None)

    # called from generate() to join together generated elements
    def concatenate(self, source):
        return " ".join(source)

    def assemble(self):
        "Yield a new text similar to existing texts."

        # get a random line beginning; convert to a list. 
        current = choice(self.beginnings)
        output = list(current)

        done = False
        for i in range(self.max):
            if current in self.ngrams:
                possible_next = self.ngrams[current]
                next = choice(possible_next)
                if next is None:
                    # This is the final item!
                    done = True
                    break
                yield next
                output.append(next)
                # get the last N entries of the output; we'll use this to look up
                # an ngram in the next iteration of the loop
                current = tuple(output[-self.order:])
            else:
                break

    chain = assemble
  
if __name__ == '__main__':
    import sys
    generator = MarkovGenerator.loadlines(sys.stdin, order=1, max=500)
    for i in range(14):
        print " ".join(list(generator.assemble()))
