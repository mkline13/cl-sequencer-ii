from parser import parse
import bisect


class Sequence:
    def __init__(self, input_string, ticks_per_beat):
        self.input_string = input_string
        self.tpb = ticks_per_beat
        self.length = 0

        self.events = []
        self.generate_events(self.input_string, self.tpb)

    def generate_events(self, input_string, ticks_per_beat):
        raw_events = parse(input_string)

        # calculate in-loop playback time for all events
        for i, event in enumerate(raw_events):
            code, args, kwargs = event
            playback_time = i * ticks_per_beat
            new_event = SequenceEvent(self, code, args, kwargs, i, playback_time)

            self.events.append(new_event)

        self.length = len(self.events) * self.tpb
        self.calculate_playback_times(-1)

    def calculate_playback_times(self, current_time):
        for event in self.events:
            event.calc_next_playback_time(current_time)

    def get_current_events(self, current_time):
        return [event for event in self.events if current_time >= event.next_playback_time]

    def print_events(self):
        for event in self.events:
            print(event)


class SequenceEvent:
    def __init__(self, sequence, code, args, kwargs, index, playback_time):
        self.sequence = sequence

        self.code = code
        self.args = args
        self.kwargs = kwargs

        self._index = index
        self._loop_playback_time = playback_time

        self.modified_loop_playback_time = playback_time
        self.next_playback_time = self.modified_loop_playback_time

    def calc_next_playback_time(self, current_time):
        if current_time > self.next_playback_time:
            next_repeat_start_time = (current_time // self.sequence.length + 1) * self.sequence.length
            self.next_playback_time = next_repeat_start_time + self.modified_loop_playback_time

    def __str__(self):
        return str((self.code, self.args, self.kwargs, self.next_playback_time))

    def __repr__(self):
        return f"Event({self.code}, {self.args}, {self.kwargs}, {self._index}, {self._loop_playback_time})"


if __name__ == '__main__':
    s = Sequence("ksk(10)ks ", 240)
    s.print_events()
    print()
    s.calculate_playback_times(0)
    s.print_events()
