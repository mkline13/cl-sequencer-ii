
VALID_EVENT_CODES = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.'
VALID_KEYWORD_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ&%$#@*+=~?'
DIGITS_ALL = '1234567890'
DIGITS_NONZERO = '123456789'


class SeqParserError(Exception):
    pass


# Todo: rewrite parser to use functional form with the following return values: err, [parsed, values], 'remaining'
# and get rid of Python Exception handling for parser errors
# hopefully this will improve the quality of the error messages


class ParserString:
    def __init__(self, input_string):
        self._input_string = input_string
        self._remaining = list(input_string) + ['<END>']

    @property
    def input_string(self):
        return self._input_string

    @property
    def remaining(self):
        return ''.join(self._remaining[:-1])

    def __len__(self):
        return len(self._remaining) - 1

    def peek(self):
        return self._remaining[0]

    def consume(self):
        char = self._remaining.pop(0)
        return char


def parse_char(inp, valid_chars):
    if inp.peek() in valid_chars:
        return inp.consume()
    else:
        return ''


def parse_chars(inp, valid_chars):
    out = ''
    while inp.peek() in valid_chars:
        out += inp.consume()
    return out


def parse_number(inp):
    if inp.peek() == "<END>":
        return None

    out = ''

    # parse negative sign
    out += parse_char(inp, '-')

    # parse first digit
    first_digit = parse_char(inp, DIGITS_ALL)
    out += first_digit

    if first_digit == '':
        if out == '':
            return None
        else:
            raise SeqParserError(f"Invalid first digit: {inp.remaining}")

    elif first_digit == '0':
        point = parse_char(inp, '.')

        if point == '.':
            out += point

            # parse digits after '.'
            out += parse_chars(inp, DIGITS_ALL)
        else:
            raise SeqParserError(f"Leading zeros not allowed: {out + inp.remaining}")

    else: # if first digit is 1-9
        # parse other digits before '.'
        out += parse_chars(inp, DIGITS_ALL)

        point = parse_char(inp, '.')

        if point == '.':
            out += point

            # parse digits after '.'
            out += parse_chars(inp, DIGITS_ALL)

    if out:
        return float(out)
    else:
        return None


def parse_comma_sep(inp):
    comma = parse_char(inp, ',')
    whitespace = parse_chars(inp, ' ')


def parse_args(inp):
    out = []
    while True:
        num = parse_number(inp)
        if num is None:
            return out
        else:
            out.append(num)
            parse_comma_sep(inp)


def parse_kwargs(inp):
    out = {}
    while True:
        result = parse_kwarg(inp)
        if result is None:
            return out
        else:
            key, value = result
            out[key] = value
            parse_comma_sep(inp)


def parse_kwarg(inp):
    key = parse_keyword(inp)

    if not key:
        return None

    colon = parse_char(inp, ':')

    if not colon:
        raise SeqParserError(f"Invalid keyword argument '{key}', requires a colon. Remaining: '{inp.remaining}'")

    value = parse_number(inp)

    if not value:
        raise SeqParserError(f"Invalid keyword argument '{key}', no value following the colon. Remaining: '{inp.remaining}'")

    return key, value


def parse_keyword(inp):
    out = ''
    out += parse_chars(inp, VALID_KEYWORD_CHARS)
    return out


def parse_parameters(inp):
    args = []
    kwargs = {}

    open_paren = parse_char(inp, '(')

    if open_paren:
        args = parse_args(inp)
        kwargs = parse_kwargs(inp)
        close_paren = parse_char(inp, ')')
        if close_paren:
            return args, kwargs
        else:
            raise SeqParserError(f"Parenthesis not closed. Remaining: '{inp.remaining}'")
    else:
        return args, kwargs


def parse_event(inp):
    code = ''
    args = []
    kwargs = {}

    code = parse_char(inp, VALID_EVENT_CODES + '<END>')
    if code == '<END>':
        return None
    elif code == '':
        raise SeqParserError(f"Invalid event code: '{inp.remaining}'")

    args, kwargs = parse_parameters(inp)

    return code, args, kwargs


def parse_sequence(inp):
    events = []
    while True:
        event = parse_event(inp)
        if event is None:
            return events
        else:
            events.append(event)


def parse(input_string):
    inp = ParserString(input_string)
    return parse_sequence(inp)