from helpers import register


class Event:
    def __init__(self, code, output, params, time):
        self.code = code
        self.output = output
        self.params = params

        self.time = time
        self.offset = 0

    @property
    def play_time(self):
        return self.time + self.offset


def create_event(default_params, output, code, args, kwargs, time):
    params = {}

    # fill in defaults as well as args
    for i, (k, v) in enumerate(default_params):
        if i < len(args):
            expected_type = type(v)
            if expected_type is int:
                user_val = int(args[i])
            elif expected_type is float:
                user_val = float(args[i])
            params[k] = user_val
        else:
            params[k] = v

    # fill in kwargs
    for k, v in kwargs.items():
        if k in params:
            params[k] = v

    return Event(code, output, params, time)


sequencer_event_bindings = {}


@register('.', sequencer_event_bindings)
def rest(code, args, kwargs, time):
    return create_event([], "rest", code, args, kwargs, time)


@register('k', sequencer_event_bindings)
def kick(code, args, kwargs, time):
    defaults = [
        ('n', 36),    # midi note number
        ('v', 127),   # velocity
        ('c', 1),     # channel
        ('%', 1.0),   # probability
        ('rv', 0.0),  # random velocity
        ('l', 10),    # note length (ticks)
    ]
    return create_event(defaults, "drum", code, args, kwargs, time)


@register('s', sequencer_event_bindings)
def snare(code, args, kwargs, time):
    defaults = [
        ('n', 38),    # midi note number
        ('v', 127),   # velocity
        ('c', 1),     # channel
        ('%', 1.0),   # probability
        ('rv', 0.0),  # random velocity
        ('l', 10),    # note length (ticks)
    ]
    return create_event(defaults, "drum", code, args, kwargs, time)


@register('h', sequencer_event_bindings)
def hihat(code, args, kwargs, time):
    defaults = [
        ('n', 42),    # midi note number
        ('v', 127),   # velocity
        ('c', 1),     # channel
        ('%', 1.0),   # probability
        ('rv', 0.0),  # random velocity
        ('l', 10),    # note length (ticks)
    ]
    return create_event(defaults, "drum", code, args, kwargs, time)

