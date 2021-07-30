import re


class Parser:
    def __init__(self):
        self.tokens = None
        self.current_state = None
        self.events = None

    def parse(self, sequence_string):
        self.tokens = self.tokenize(sequence_string)
        self.current_state = PSReadEvents(self)
        self.events = []

        while len(self.tokens) > 0:
            self.current_state.handle_token(self)

        return self.events

    def change_state(self, next_state, *args, **kwargs):
        self.current_state.on_exit(self)
        self.current_state = next_state(self, *args, **kwargs)

    def get_current_token(self):
        if self.tokens:
            return self.tokens[0]
        else:
            return None

    def lookahead(self, amount=1):
        if amount < len(self.tokens):
            return self.tokens[amount]
        else:
            return None

    def advance(self):
        self.tokens.pop(0)

    def get_current_event(self):
        return self.events[-1]

    @staticmethod
    def tokenize(input_str):
        input_str = list(input_str)
        tokens = []
        current = []

        in_parentheses = False
        while len(input_str) > 0:
            char = input_str.pop(0)
            if not in_parentheses:
                if re.match("[a-zA-Z ]", char) is not None:
                    tokens.append(("EVENT", char))
                elif char == "(":
                    tokens.append(("PUNC", char))
                    in_parentheses = True
                else:
                    raise SyntaxError(f"Invalid character: {char}")
            else:
                if re.match(r"[-\w~!@$%^&*. ]", char) is not None:
                    current.append(char)
                elif char == ":":
                    key = Parser._format_key("".join(current))
                    tokens.append(("KEY", key))
                    current = []
                    tokens.append(("PUNC", char))
                elif char == ",":
                    val = Parser._format_val("".join(current))
                    tokens.append(("VAL", val))
                    current = []
                    tokens.append(("PUNC", char))
                elif char == ")":
                    val = float("".join(current).strip(" "))
                    tokens.append(("VAL", val))
                    current = []
                    tokens.append(("PUNC", char))
                    in_parentheses = False
                else:
                    raise SyntaxError(f"Invalid character: {char}")
        return tokens

    @staticmethod
    def _format_key(key_str):
        key = key_str.strip(" ")
        if re.match(r"^[a-zA-Z~!@$%&*][\w~!@$%&*]*$", key) is not None:
            return key
        else:
            raise SyntaxError("Parameter keys must not start with numbers or certain characters. Must contain no spaces. Format: ^[a-zA-Z~!@$%&*][\w~!@$%&*]*$")

    @staticmethod
    def _format_val(val_str):
        val = float(val_str.strip(" ").rstrip("."))
        return val


class ParserState:
    def __init__(self, parser, *args, **kwargs):
        self.initialize(*args, **kwargs)
        self.on_enter(parser)

    def initialize(self, *args, **kwargs):
        pass

    def on_enter(self, parser):
        pass

    def on_exit(self, parser):
        pass

    def handle_token(self, parser):
        pass


class PSReadEvents(ParserState):
    def handle_token(self, parser):
        t_type, t_value = token = parser.get_current_token()
        if t_type == 'EVENT':
            parser.events.append({"code": t_value})
            parser.advance()
        elif t_value == '(' and parser.lookahead()[0] == 'VAL':
            parser.change_state(PSReadArgs)
            parser.advance()
        elif t_value == '(' and parser.lookahead()[0] == 'KEY':
            parser.change_state(PSReadKwargs)
            parser.advance()
        else:
            raise SyntaxError(f"Unexpected token: {token}")


class PSReadArgs(ParserState):
    def on_enter(self, parser):
        parser.get_current_event()["args"] = []

    def handle_token(self, parser):
        t_type, t_value = token = parser.get_current_token()
        if t_type == 'VAL':
            parser.get_current_event()["args"].append(t_value)
            parser.advance()
        elif t_value == ',' and parser.lookahead()[0] == 'VAL':
            parser.advance()
        elif t_value == ',' and parser.lookahead()[0] == 'KEY':
            parser.change_state(PSReadKwargs)
            parser.advance()
        elif t_value == ')':
            parser.change_state(PSReadEvents)
            parser.advance()
        else:
            raise SyntaxError(f"Unexpected token: {token}")


class PSReadKwargs(ParserState):
    def on_enter(self, parser):
        parser.get_current_event()["kwargs"] = {}

    def handle_token(self, parser):
        t_type, t_value = token = parser.get_current_token()
        if t_type == 'KEY' and parser.lookahead(1)[1] == ':' and parser.lookahead(2)[0] == 'VAL':
            parser.get_current_event()["kwargs"][t_value] = parser.lookahead(2)[1]
            parser.advance()
            parser.advance()
            parser.advance()
        elif t_value == ',' and parser.lookahead()[0] == 'KEY':
            parser.advance()
        elif t_value == ')':
            parser.change_state(PSReadEvents)
            parser.advance()
        else:
            raise SyntaxError(f"Unexpected token: {token}")


def parse(input_str):
    events = Parser().parse(input_str)
    return events


if __name__ == '__main__':
    test_str = "skk(-10.100, 20, j:33) k(55, 22, %bab:505, v:100)s"
    e = parse(test_str)
    for i in e:
        print(i)