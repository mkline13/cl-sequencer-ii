from parser import parse


class Sequence:
    def __init__(self, input_string, events, ticks_per_beat):
        self.input_string = input_string
        self.events = events
        self.tpb = ticks_per_beat
        self.length = len(events) * self.tpb

        self.calc_all_playback_times(-1)

        self.played_events = []

    @staticmethod
    def new_from_string(input_string, ticks_per_beat):
        raw_events = parse(input_string)
        events = []

        for i, event in enumerate(raw_events):
            code, args, kwargs = event
            playback_time = i * ticks_per_beat
            events.append(Event(code, args, kwargs, i, playback_time))

        return Sequence(input_string, events, ticks_per_beat)

    def calc_all_playback_times(self, current_time):
        for event in self.events:
            self.calc_next_playback(event, current_time)

    def calc_next_playback(self, event, current_time):
        if current_time > event.next_playback_time:
            next_repeat_start_time = (current_time // self.length + 1) * self.length
            event.next_playback_time = next_repeat_start_time + event.modified_loop_playback_time

    def get_current_events(self, current_time):
        self.played_events = [e for e in self.events if current_time >= e.next_playback_time]
        return self.played_events

    def recalc_played_events(self, current_time):
        for event in self.played_events:
            self.calc_next_playback(event, current_time)

    def print_events(self):
        for e in self.events:
            print(e)


class Event:
    def __init__(self, code, args, kwargs, index, playback_time):
        self.code = code
        self.args = args
        self.kwargs = kwargs

        self._index = index
        self._loop_playback_time = playback_time

        self.modified_loop_playback_time = playback_time
        self.next_playback_time = self.modified_loop_playback_time

    def __str__(self):
        return str((self.code, self.args, self.kwargs, self.next_playback_time))

    def __repr__(self):
        return f"Event({self.code}, {self.args}, {self.kwargs}, {self._index}, {self._loop_playback_time})"


if __name__ == '__main__':
    s = Sequence.new_from_string("ksk(10)ks ", 240)
    s.print_events()
    print()
    s.calc_all_playback_times(0)
    s.print_events()

    print()
    time = 800
    events = s.get_current_events(time)
    print(events)
    for e in events:
        s.calc_next_playback(e, time)
