

class Event:
    def __init__(self, time, msg=""):
        self.time = time
        self.msg = msg

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, other):
        return self.time == other.time


class Sequence:
    def __init__(self, events, ticks_per_event=240):
        self.events = events
        self.tpe = ticks_per_event
        self.duration = len(self.events) * self.tpe

        self._prev_time = -1
        self._current_loop = list(self.events)
        self._next_loop = []

    def get_next_events(self, time):
        loop_time = time % self.duration
        print("TIME: lp prev ", loop_time, self._prev_time)
        if loop_time >= self._prev_time:
            # if the loop has not restarted at the beginning
            while self._current_loop and self._current_loop[0].time <= loop_time:
                event = self._current_loop.pop(0)
                yield event
                self._next_loop.append(event)
        else:
            # if the loop has restarted at the beginning
            # finish out the _current_loop list
            while self._current_loop:
                event = self._current_loop.pop(0)
                yield event
                self._next_loop.append(event)

            # swap current with next list and sort
            self._swap()

            # catch up at beginning
            while self._current_loop and self._current_loop[0].time <= loop_time:
                event = self._current_loop.pop(0)
                yield event
                self._next_loop.append(event)

        self._prev_time = loop_time

    def seek(self, time):
        while self._current_loop and self._current_loop[0].time <= time:
            event = self._current_loop.pop(0)
            print("SKIP", event.time, event.msg)
            self._next_loop.append(event)

        if not self._current_loop:
            self._swap()

    def _swap(self):
        self._current_loop = sorted(self._next_loop)
        self._next_loop = []


if __name__ == '__main__':
    events = [Event(0), Event(5), Event(10), Event(15)]

    s = Sequence(events, ticks_per_event=5)

    time = 2
    for e in s.get_next_events(time):
        print(time, e.time)

    time = 23
    for e in s.get_next_events(time):
        print(time, e.time)



    #s.seek(40)
