import transport
import event_handlers
import scheduler


class Player:
    event_code_map = {
        "k": event_handlers.DrumEventHandler(36, 127, 0, 30),
        "s": event_handlers.DrumEventHandler(39, 127, 0, 30),
        "h": event_handlers.DrumVelCycleEventHandler(42, [20, 60, 100, 127], 1, 30),
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

            # execute the events' high priority functions
            for event in current_events:
                self.exec_high_priority(event)

            # this is where items in the temporary scheduler will be executed
            scheduler.play_current_events(current_time)

            # execute the events' low priority functions
            for event in current_events:
                self.exec_low_priority(event)


            # calculate timing for next occurrence of played events
            # other precalcs will be done here as well
            # for event in current_events:
            #     event.calc_next_playback_time(current_time)

            for event in current_events:
                self.exec_precalcs(event, current_time)

            # if self.transport.get_elapsed_ticks() > 10000:
            #     self.stop()

    def stop(self):
        self.transport.stop()
        self.running = False
        scheduler.flush_events()

    def exec_high_priority(self, event):
        if event.code in self.event_code_map:
            self.event_code_map[event.code].high_priority(event)

    def exec_low_priority(self, event):
        if event.code in self.event_code_map:
            self.event_code_map[event.code].low_priority(event)

    def exec_precalcs(self, event, current_time):
        if event.code in self.event_code_map:
            self.event_code_map[event.code].pre_calc(event, current_time)


if __name__ == '__main__':
    import sequence
    p = Player(None)
    # p.sequences.append(sequence.Sequence("kkskkk.s", p.transport.tpqn))
    # p.sequences.append(sequence.Sequence("k....", p.transport.tpqn / 4))
    # p.sequences.append(sequence.Sequence("h", p.transport.tpqn / 4))

    p.sequences.append(sequence.Sequence("k", p.transport.tpqn))
    p.sequences.append(sequence.Sequence("k....", p.transport.tpqn / 4))
    p.sequences.append(sequence.Sequence(".s", p.transport.tpqn))
    p.sequences.append(sequence.Sequence(".hhh", p.transport.tpqn / 4))
    p.play()