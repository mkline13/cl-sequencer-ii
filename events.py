from helpers import register


class Event:
    def __init__(self, code, destination, payload, time):
        self.code = code
        self.destination = destination
        self.payload = payload

        self.time = time
        self.offset = 0

    @property
    def play_time(self):
        return self.time + self.offset


def create_event(default_params, output, code, oargs, largs, time):
    params = {}

    # fill in defaults as well as args
    for i, (k, v) in enumerate(default_params):
        if i < len(oargs):
            expected_type = type(v)
            if expected_type is int:
                user_val = int(oargs[i])
            elif expected_type is float:
                user_val = float(oargs[i])
            params[k] = user_val
        else:
            params[k] = v

    # fill in kwargs
    for k, v in largs.items():
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
        ('note', 36),    # midi note number
        ('vel', 127),   # velocity
        ('chan', 1),     # channel
        ('prob', 1.0),   # probability
        ('rand_vel', 0.0),  # random velocity
        ('length', 10),    # note length (ticks)
    ]
    return create_event(defaults, "drum", code, args, kwargs, time)


@register('s', sequencer_event_bindings)
def snare(code, args, kwargs, time):
    defaults = [
        ('note', 38),    # midi note number
        ('vel', 127),   # velocity
        ('chan', 1),     # channel
        ('prob', 1.0),   # probability
        ('rand_vel', 0.0),  # random velocity
        ('length', 10),    # note length (ticks)
    ]
    return create_event(defaults, "drum", code, args, kwargs, time)


@register('h', sequencer_event_bindings)
def hihat(code, args, kwargs, time):
    defaults = [
        ('note', 42),    # midi note number
        ('vel', 127),   # velocity
        ('chan', 1),     # channel
        ('prob', 1.0),   # probability
        ('rand_vel', 0.0),  # random velocity
        ('length', 10),    # note length (ticks)
    ]
    return create_event(defaults, "drum", code, args, kwargs, time)

