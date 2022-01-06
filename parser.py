"""
format

parser(char_list: tuple) -> traceback: list of string messages, [parsed elements: Any], remaining_text: list

append to traceback if parser fails


traceback format = (currentfunc.__name__, message, remaining)
"""


def text_to_char_list(text):
    return list(text) + ['END']


def char_list_to_text(char_list):
    return ''.join(char_list[:-1])


class TraceLine:
    def __init__(self, function, message, remaining):
        self.function_name = function.__name__
        self.message = message
        self.remaining = char_list_to_text(remaining)
    
    def render(self):
        return f"{self.function_name}: {self.message}    remaining: '{self.remaining}'"
    
    
VALID_EVENT_CODES = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.'
VALID_ARG_LABELS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ&%$#@*+=~?'
DIGITS_ALL = '1234567890'
DIGITS_NONZERO = '123456789'

OPEN_PAREN = '('
CLOSED_PAREN = ')'


larg_renaming = {
    'n': "note",
    'v': "vel",
    'c': "chan",
    '~v': "rand_vel",
    '%': "prob",
    'l': "length",
}


def parse_char(char_list, allowed_chars):
    """
    Parse single char.
    """
    if char_list[0] in allowed_chars:
        return [], char_list[:1], char_list[1:]
    else:
        line = TraceLine(parse_char, f"'{char_list[0]}' not in allowed chars: '{allowed_chars}'", char_list)
        return [line], [], char_list


def parse_chars(char_list, allowed_chars):
    """
    Parse multiple chars of the same type.
    """
    i = 0
    for c in char_list:
        if c not in allowed_chars:
            break
        else:
            i += 1
    if i == 0:
        line = TraceLine(parse_chars, f"'{char_list[0]}' not in allowed chars: '{allowed_chars}'", char_list)
        return [line], [], char_list
    else:
        return [], char_list[:i], char_list[i:]


def parse_list_sep(char_list):
    """
    Parse commas + whitespace: ', ' or ' ,  ' or ',' etc.
    """
    # parse leading whitespace
    _, _, remaining = parse_chars(char_list, ' ')
    
    # parse comma
    _, comma, remaining = parse_char(remaining, ',')
    
    if not comma:
        line = TraceLine(parse_list_sep, f"not a valid list separator: no comma found", char_list)
        return [line], [], char_list
    
    # parse trailing whitespace
    _, _, remaining = parse_chars(remaining, ' ')
    
    return [], comma, remaining


def parse_int(char_list):
    """
    Parse signed integers, allow leading zeros.
    """
    # parse negative sign
    _, minus, remaining = parse_char(char_list, '-')
    
    # parse leading zeros
    trace_leading_zeros, leading_zeros, remaining = parse_chars(remaining, '0')
    
    # parse other digits
    trace_digits, digits, remaining = parse_chars(remaining, DIGITS_ALL)

    if not leading_zeros and not digits:
        line = TraceLine(parse_int, f"could not parse int, no digits found", char_list)
        trace = trace_leading_zeros + trace_digits + [line]
        return trace, [], char_list
    
    if not digits:
        return [], [0], remaining
    else:
        value = int(''.join(minus + digits))
        return [], [value], remaining


def parse_float(char_list):
    """
    Parse signed floats, allow leading zeros.
    """
    # parse negative sign
    _, minus, remaining = parse_char(char_list, '-')
    
    # parse leading zeros
    trace_leading_zeros, leading_zeros, remaining = parse_chars(remaining, '0')
    
    # parse other whole digits
    trace_digits, digits, remaining = parse_chars(remaining, DIGITS_ALL)
    
    # parse decimal point
    trace_decimal, decimal, remaining = parse_char(remaining, '.')
    
    if not decimal:
        line = TraceLine(parse_float, f"could not parse float, no decimal point", char_list)
        trace = trace_decimal + [line]
        return trace, [], char_list
    
    # parse fractional digits
    trace_frac, frac, remaining = parse_chars(remaining, DIGITS_ALL)
    
    if not leading_zeros and not digits and not frac:
        line = TraceLine(parse_float, f"could not parse float, no digits found", char_list)
        trace = trace_leading_zeros + trace_digits + trace_frac + [line]
        return trace, [], char_list
    else:
        value = float(''.join(minus + leading_zeros + digits + decimal + frac))
        return [], [value], remaining


def parse_number(char_list):
    trace_fl, fl, remaining = parse_float(char_list)
    if fl:
        return [], fl, remaining
    
    trace_integer, integer, remaining = parse_int(char_list)
    if integer:
        return [], integer, remaining
    else:
        line = TraceLine(parse_float, f"could not parse number", char_list)
        trace = trace_fl + trace_integer + [line]
        return trace, [], char_list


def parse_labeled_arg(char_list):
    """
    Parse labeled arguments in the following format:
    
    xn
    
    where x is the label and n is a numerical value
    
    """
    # parse label
    trace_label, label, remaining = parse_chars(char_list, VALID_ARG_LABELS)
    
    if not label:
        line = TraceLine(parse_labeled_arg, f"no valid label, must be one of the following: '{VALID_ARG_LABELS}'", char_list)
        return [line], [], char_list

    label_str = ''.join(label)
    
    # parse value
    trace_value, value, remaining = parse_number(remaining)
    
    if not value:
        line = TraceLine(parse_labeled_arg, f"no valid value, must be int or float", char_list)
        return trace_value + [line], [], char_list
    else:
        renamed_label = [larg_renaming.get(label_str, label_str)]
        return [], [tuple(renamed_label + value)], remaining


def parse_event_params(char_list):
    # TODO: parser works but the error codes need to be adjusted
    # parse open parenthesis
    trace_open_p, open_p, remaining = parse_char(char_list, OPEN_PAREN)
    
    if not open_p:
        line = TraceLine(parse_event_params, f"could not parse parameters, no open parenthesis '{OPEN_PAREN}'", char_list)
        return [], [[], {}], char_list
    
    _, _, remaining = parse_chars(remaining, ' ')  # absorb whitespace
    
    # parse ordered args + commas
    oargs = []
    while True:
        trace_oarg, oarg, remaining = parse_number(remaining)
        if not oarg:
            break
        else:
            oargs += oarg
            
        trace_sep, sep, remaining = parse_list_sep(remaining)
        if not sep:
            break
    
    _, _, remaining = parse_chars(remaining, ' ')  # absorb whitespace
    
    # parse labeled args  ex. '%19, b22'
    largs = {}
    while True:
        trace_larg, larg, remaining = parse_labeled_arg(remaining)
        if not larg:
            break
        else:
            key, value = larg[0]
            largs[key] = value
            
        trace_sep, sep, remaining = parse_list_sep(remaining)
        if not sep:
            break
    
    _, _, remaining = parse_chars(remaining, ' ')  # absorb whitespace
    
    # parse close parenthesis
    trace_close_p, close_p, remaining = parse_char(remaining, CLOSED_PAREN)
    
    if not close_p:
        line = TraceLine(parse_event_params, f"could not parse parameters, no closing parenthesis '{CLOSED_PAREN}'", char_list)
        return [line], [], char_list
    else:
        return [], [oargs, largs], remaining


def parse_event(char_list):
    # parse event code
    trace_code, code, remaining = parse_char(char_list, VALID_EVENT_CODES)
    if not code:
        line = TraceLine(parse_event, f"invalid event code '{char_list[0]}', must be one of: '{VALID_EVENT_CODES}'", char_list)
        return [line], [], char_list
    
    # parse params
    trace_params, params, remaining = parse_event_params(remaining)
    
    if not params:
        line = TraceLine(parse_event, f"Parameter parsing failed", char_list)
        return trace_params + [line], [], char_list
    
    oargs, largs = params
    return [], (code[0], oargs, largs), remaining


def parse_sequence(char_list):
    """
    Parse a sequence of events into a list
    """
    # get all events
    remaining = char_list[:]
    events = []
    while True:
        trace_event, event, remaining = parse_event(remaining)
        if event:
            events += [event]
        else:
            break
    
    # success if whitespace or "END" is detected
    if remaining[0] == ' ' or remaining[0] == 'END':
        return [], events, remaining
    else:
        line = TraceLine(parse_sequence, f"unexpected chars found in sequence: '{char_list_to_text(remaining)}'", char_list)
        trace = trace_event + [line]
        return trace, [], char_list


def parse(input_string):
    """
    Provides an interface to the functionality of this module for other parts of the program to use.
    """
    char_list = text_to_char_list(input_string)
    trace, result, remaining = parse_sequence(char_list)
    return trace, result, remaining


if __name__ == '__main__':
    trace, sequence, remaining = parse("x(10)y(v100, ~v32, %66)ksks")
    print(sequence)