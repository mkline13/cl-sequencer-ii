
sequence = [
    {"code": "k"},
    {"code": "s"},
    {"code": "h"},
    {"code": "k"}
]


class Event:
    def __init__(self, callback, args=[], kwargs={}):
        self.time = 0
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def play(self):
        self.callback(self, self.args, self.kwargs)

    def __str__(self):
        return f"<Event time={self.time} args={self.args}, kwargs={self.kwargs}>"


class Sequence:
    def __init__(self, events, ticks_per_event):
        self.events = events
        self.num_steps = len(self.events)
        self.ticks_per_event = ticks_per_event
        self.duration = len(self.events) * self.ticks_per_event

        for i, e in enumerate(self.events):
            e.time = i * self.ticks_per_event

    def __str__(self):
        events = '\n'.join(["  " + str(e) for e in self.events])
        return f"<Sequence tpe={self.ticks_per_event} dur={self.duration}>\n" + events


class Track:
    def __init__(self, sequence):
        self.sequence = sequence

        self._playhead = 0
        self._prev_time = -1

    def play(self, time):
        time = time % self.sequence.duration
        if time > self._prev_time:
            while time >= self.next_event().time > self._prev_time:
                self.advance()
        else:    # When the sequence wraps back around and repeats
            while self.next_event().time > self._prev_time or self.next_event().time <= time:
                self.advance()

        self._prev_time = time

    def advance(self):
        self.next_event().play()
        self._playhead = (self._playhead + 1) % self.sequence.num_steps

    def next_event(self):
        return self.sequence.events[self._playhead]



def test_callback(event, args, kwargs):
    print("test play:", event)


if __name__ == '__main__':
    events = [
        Event(test_callback, [1]),
        Event(test_callback, [2]),
        Event(test_callback, [3]),
        Event(test_callback, [4], {"k": 22}),
    ]

    s = Sequence(events, 240)
    print(s)
    print()

    t = Track(s)

    for i in [0, 100, 400, 600, 800, 1000, 2000]:
        print("PLAY AT: ", i, t._playhead)
        t.play(i)
