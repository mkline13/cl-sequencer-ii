

class Event:
    def __init__(self, time, callback, args, kwargs, flush=True):
        self.time = time
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.played = False
        self.flush = flush

    def play(self):
        self.callback(*self.args, **self.kwargs)
        self.played = True


upcoming_events = []


def play_current_events(current_time):
    global upcoming_events

    for event in upcoming_events:
        if event.time <= current_time:
            event.play()

    upcoming_events = [event for event in upcoming_events if event.played == False]


def add_event(time, callback, args, kwargs, flush=True):
    global upcoming_events
    upcoming_events.append(Event(time, callback, args, kwargs, flush))


def flush_events():
    global upcoming_events
    for event in upcoming_events:
        if event.flush == False:
            event.play()
    upcoming_events = []