import midi
import random


def drum(scheduler, note, velocity, random_velocity, probability, channel):
    velocity = int(velocity - random.randint(0, random_velocity))
    channel = int(channel)
    if random.random() <= probability:
        midi.note_on(note, velocity, channel)

        # create the callback for the note off event in the scheduler
        def note_off_callback():
            midi.note_off(note, channel)

        # schedule the note off


def rest(event, scheduler):
    pass


def kick(event, scheduler):
    # defaults
    params = {
        "vel": 100,
        "rvel": 0,
        "prob": 1
    }

    # ordered args
    for param_name, arg in zip(["vel", "rvel", "prob"], event.args):
        params[param_name] = arg

    # kwargs
    params.update(event.kwargs)

    # send output
    drum(scheduler, 36, params["vel"], params["rvel"], params["prob"], 1)


def snare(event, scheduler):
    # defaults
    params = {
        "vel": 100,
        "rvel": 0,
        "prob": 1
    }

    # ordered args
    for param_name, arg in zip(["vel", "rvel", "prob"], event.args):
        params[param_name] = arg

    # kwargs
    params.update(event.kwargs)

    # send output
    drum(scheduler, 38, params["vel"], params["rvel"], params["prob"], 1)


def hat(event, scheduler):
    # defaults
    params = {
        "vel": 100,
        "rvel": 0,
        "prob": 1
    }

    # ordered args
    for param_name, arg in zip(["vel", "rvel", "prob"], event.args):
        params[param_name] = arg

    # kwargs
    params.update(event.kwargs)

    # send output
    drum(scheduler, 42, params["vel"], params["rvel"], params["prob"], 1)


def block(event, scheduler):
    # defaults
    params = {
        "vel": 100,
        "rvel": 50,
        "prob": 0.5
    }

    # ordered args
    for param_name, arg in zip(["vel", "rvel", "prob"], event.args):
        params[param_name] = arg

    # kwargs
    params.update(event.kwargs)

    # send output
    drum(scheduler, 37, params["vel"], params["rvel"], params["prob"], 1)


def print_event(event, scheduler):
    print("PLAYING:", event.code)


class EventDispatch:
    def __init__(self):
        self.mapping = {
            "k": kick,
            "b": block,
            "s": snare,
            "h": hat,
            ".": rest,
            "p": print_event
        }

    def dispatch(self, event, scheduler):
        self.mapping.get(event.code, rest)(event, scheduler)
