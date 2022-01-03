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


class Scheduler:
    def __init__(self):
        self.upcoming_events = []

    def play_current_events(self, current_time):
        for event in self.upcoming_events:
            if event.time <= current_time:
                event.play()
        self.upcoming_events = [event for event in upcoming_events if event.played == False]

    def add_event(self, time, callback, args, kwargs, flush=True):
        self.upcoming_events.append(Event(time, callback, args, kwargs, flush))

    def flush_events(self):
        for event in self.upcoming_events:
            if not event.flush:
                event.play()
        self.upcoming_events = []
