import lepl

class _Token(object):
    def __init__(self, value):
        self.value = value
        self.tail = None

    def __radd__(self, other):
        return other + [self]

    def __repr__(self):
        r = repr(self.value).lstrip('u')
        return "%s (%s)" % (r, type(self).__name__[1].upper())

class _Delimiter(_Token): pass
class _Number(_Token): pass
class _Float(_Number): pass
class _Integer(_Number): pass
class _Word(_Token): pass

tokens = (lepl.Token(r'[A-Za-z]+') >> _Word) | \
          (lepl.Token(r'\-?[0-9]+') >> int >> _Integer) | \
          (lepl.Token(lepl.Float()) >> float >> _Float) | \
          (lepl.Token(r'[,;]') >> _Delimiter)

lexer = tokens[1:].get_parse()

def tokenize(string):
    """Return sequence of tokens in ``string``.

    The letter in the parenthesis denotes the token type.

    >>> tokenize("John Smith, Male")
    ['John' (W), 'Smith' (W), ',' (D), 'Male' (W)]

    >>> tokenize("M 16 yrs, John Smith")
    ['M' (W), 16 (I), 'yrs' (W), ',' (D), 'John' (W), 'Smith' (W)]

    >>> tokenize("Temperature -16 C")
    ['Temperature' (W), -16 (I), 'C' (W)]

    >>> tokenize("Temperature -16.0 C")
    ['Temperature' (W), -16.0 (F), 'C' (W)]
    """

    return lexer(string)
