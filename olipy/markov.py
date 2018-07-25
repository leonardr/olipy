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
        corpus = MarkovGenerator(order, max)
        corpus.add(f.read())
        return corpus

    @classmethod
    def loadlines(cls, f, order=1, max=500):
        """Load from a filehandle that defines one text per line."""
        corpus = MarkovGenerator(order, max)
        if not hasattr(f, 'read'):
            # Not a file-type object. Treat it as a multi-line string.
            f = f.split("\n")
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
        for token in current:
            yield token

        done = False
        for i in range(self.max):
            if current in self.ngrams:
                possible_next = self.ngrams[current]
                next = choice(possible_next)
                if next is None:
                    # This is the final item!
                    done = True
                    break
                yield self.modify(next)
                output.append(next)
                # get the last N entries of the output; we'll use this to look up
                # an ngram in the next iteration of the loop
                current = tuple(output[-self.order:])
            else:
                break

    generate = assemble
    chain = assemble

    def modify(self, token):
        """Modify a token before yielding it."""
        return token

class BracketMatchingMarkovGenerator(MarkovGenerator):

    """A generator that tries to ensure balanced brackets and double quotes.

    It's not perfect, but it's a lot better than nothing.
    """

    def __init__(self, *args, **kwargs):
        super(BracketMatchingMarkovGenerator, self).__init__(*args, **kwargs)
        self.useful_tokens = set([])

    def tokenize(self, text):
        tokens = super(BracketMatchingMarkovGenerator, self).tokenize(text)
        for token in tokens:
            for closing in ['"', ")", "]", "}"]:
                if token.endswith(closing):
                    self.useful_tokens.add(token)
        return tokens

    def assemble(self):
        self.stack = []
        for x in super(BracketMatchingMarkovGenerator, self).assemble():
            yield x

    def modify(self, token_to_yield):
        # Is there an opening bracket in this token?
        for opening, closing in ['""', "()", "[]", "{}"]:
            if opening in token_to_yield:
                index = token_to_yield.find(opening)
                if token_to_yield.find(closing, index+1) == -1:
                    self.stack.append(closing)
            elif closing in token_to_yield:
                # We are closing a bracket. Is there an open bracket?
                if len(self.stack) == 0:
                    #Nope.
                    token_to_yield = token_to_yield.replace(closing, "")
                elif closing != self.stack[-1]:
                    # Force it to be the right kind of bracket.
                    token_to_yield = token_to_yield.replace(
                        closing, self.stack[-1], 1)
                    self.stack.pop()
                else:
                    # It's already the right kind of bracket.
                    self.stack.pop()

        if len(self.stack) > 0:
            # If we modify this token by appending the closing bracket
            # on top of the stack, would we get a token that exists in
            # the corpus?
            check_for = token_to_yield + self.stack[-1]
            if check_for in self.useful_tokens:
                self.stack.pop()
                return check_for
        # No luck. Return the original token.
        return token_to_yield
  
if __name__ == '__main__':
    import sys
    generator = MarkovGenerator.loadlines(sys.stdin, order=1, max=500)
    for i in range(14):
        print " ".join(list(generator.assemble()))
