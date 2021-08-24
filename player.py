import transport, midi


class Player:
    midi_map = {
        "k": 36,
        "s": 39,
        "h": 42,
    }

    def __init__(self, app):
        self.app = app
        self.transport = transport.Transport(bpm=120, tpqn=480)
        self.sequences = []

        self.running = False

    def play(self):
        # setup
        current_time = self.transport.get_elapsed_ticks()

        # precalculate timing and anything else for upcoming events
        for seq in self.sequences:
            seq.calculate_playback_times(current_time)

        # playback loop
        self.running = True
        self.transport.start()

        while self.running:
            current_time = self.transport.get_elapsed_ticks()

            current_events = []

            # retrieve current events from all sequences
            for seq in self.sequences:
                current_events += seq.get_current_events(current_time)

            # execute the events
            for event in current_events:
                self.exec_event(event)

            # this is where items in the temporary scheduler will be executed

            # then maybe execute low-priority functionality of events (such as scheduling note-offs)

            # calculate timing for next occurrence of played events
            # other precalcs will be done here as well
            for event in current_events:
                event.calc_next_playback_time(current_time)

            if self.transport.get_elapsed_ticks() > 10000:
                self.stop()

    def stop(self):
        self.transport.stop()
        self.running = False

    def exec_event(self, event):
        if event.code in self.midi_map.keys():
            midi.note_on(self.midi_map[event.code], 127, 1)


if __name__ == '__main__':
    import sequence
    p = Player(None)
    p.sequences.append(sequence.Sequence("kkskkk s", p.transport.tpqn / 2))
    p.sequences.append(sequence.Sequence("h", p.transport.tpqn / 4))
    p.play()