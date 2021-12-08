from parser import parse


class SEvent:
    def __init__(self, code, args, kwargs, time):
        # How to play
        self.code = code
        self.args = args
        self.kwargs = kwargs

        # When to play
        self.time = time
        self.offset = 0

    @property
    def play_time(self):
        return self.time + self.offset


class Sequence:
    def __init__(self, input_string, tpb):
        self.input_string = input_string
        self.__tpb = tpb  # ticks per beat

        # parse and transform input string
        raw_sequence = parse(input_string)
        self.events = [SEvent(code, args, kwargs, i * self.__tpb) for i, (code, args, kwargs) in enumerate(raw_sequence)]

    @property
    def tpb(self):
        return self.__tpb

    @tpb.setter
    def tpb(self, value):
        self.__tpb = value
        for i, event in enumerate(self.events):
            event.time = i * self.__tpb

    @property
    def length(self):
        return len(self.events) * self.__tpb

    def print(self):
        indent = "  "
        print(f"Sequence: '{self.input_string}'")
        for event in self.events:
            time = str(event.play_time).rjust(5)
            print(f"{indent}{time} - {event.code.ljust(2)} {event.args} {event.kwargs}")


if __name__ == '__main__':
    s = Sequence('kksshh(300)', 480)
    s.print()
    s.tpb = 120
    s.print()
