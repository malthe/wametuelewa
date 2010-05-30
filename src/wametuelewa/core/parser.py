import lepl
from . import tokens

@lepl.function_matcher_factory()
def wrapper(type_):
    def matcher(support, stream):
        if stream and isinstance(stream[0], type_):
            return (stream[0], stream[1:])
    return matcher

Delimiter = lepl.Drop(wrapper(tokens._Delimiter))
Float = wrapper(tokens._Float)
Integer = wrapper(tokens._Integer)
Number = wrapper(tokens._Number)
Word = wrapper(tokens._Word)

example_phrase = [
    tokens._Word("John"),
    tokens._Word("Smith"),
    tokens._Delimiter(","),
    tokens._Integer(16),
    tokens._Word("M"),
    ]

def missing(label):
    """Provides feedback when a matcher fails.

    This function is commonly applied using the :class:`First`
    operator (short-hand: ``\%``).

    We'll consider the following example phrase:

    >>> example_phrase
    ['John' (W), 'Smith' (W), ',' (D), 16 (I), 'M' (W)]

    The following matcher illustrates the usage:

    >>> matcher = Word[1:] & lepl.Optional(
    ...     Delimiter & (Number & Word) % missing('age and sex'))

    Omitting the last token from our example phrase, we get the
    following feedback:

    >>> parse(matcher, example_phrase[:-1])[0]
    u'age and sex'

    To improve feedback, we can provide help for each case
    individually:

    >>> matcher = Word[1:] % missing('name') & lepl.Optional(
    ...     Delimiter & Number % missing('age') & Word % missing('sex'))

    The ``\%`` operator binds more strongly and parentheses are
    unnecessary for the most part.

    >>> parse(matcher, example_phrase[:-2])[0]
    u'age'
    >>> parse(matcher, example_phrase[:-1])[0]
    u'sex'

    Note that the full phrase still returns a match:

    >>> parse(matcher, example_phrase)
    ['John' (W), 'Smith' (W), 16 (I), 'M' (W)]

    So far we've dealt with missing input only; the function also
    guards against incorrect input:

    >>> phrase = example_phrase[:-2] + example_phrase[:1]
    >>> parse(matcher, phrase)[0]
    u'age'

    Finally, the function operates within a more complex environment
    of multiple paths.

    >>> matcher = Word[1:] % missing('name') & \\
    ...     lepl.Optional(
    ...         Delimiter & Number % missing('age') & Word % missing('sex')) & \\
    ...     lepl.Optional(
    ...         Delimiter & Number % missing('age'))

    >>> parse(matcher, example_phrase[:-2])[0]
    u'age'

    Omitting only the last token, this particular matcher chooses the
    path through the second optional clause and succeeds:

    >>> parse(matcher, example_phrase[:-1])
    ['John' (W), 'Smith' (W), 16 (I)]
    """

    return lepl.Any()[:] ** lepl.make_error(label)

def parse(matcher, tokens):
    """Matches a complete sequence of tokens using ``matcher``, or
    throws the error raised at the deepest recursion if there was no
    complete match.

    In the following, we'll consider the following example phrase,
    copied here for the sake of documentation:

    >>> example_phrase
    ['John' (W), 'Smith' (W), ',' (D), 16 (I), 'M' (W)]

    That's two words, a delimiter, an integer and a word (any number
    of consecutive letters constitutes a word). Here's a very simple
    matcher for the example phrase:

    >>> matcher = Word[2] & Delimiter & Number & Word

    Since the delimiter is automatically dropped, the result becomes:

    >>> parse(matcher, example_phrase)
    ['John' (W), 'Smith' (W), 16 (I), 'M' (W)]

    The :mod:`lepl` library provides a number of ways to combine and
    modify parsers. For instance, we could define an optional
    component:

    >>> matcher = Word[1:] & lepl.Optional(Delimiter & Number & Word)

    This would still parse the complete example phrase, but also the
    subset of the first two tokens:

    >>> parse(matcher, example_phrase)
    ['John' (W), 'Smith' (W), 16 (I), 'M' (W)]
    >>> parse(matcher, example_phrase[:2])
    ['John' (W), 'Smith' (W)]
    """

    matcher.config.no_full_first_match()

    error = None
    match = None
    depth = -1

    for result, remaining in matcher.match(tokens):
        if remaining:
            continue
        for index, token in enumerate(result):
            if isinstance(token, lepl.Error):
                if index > depth:
                    error = token
                    depth = index
                break
        else:
            return result

    return error
