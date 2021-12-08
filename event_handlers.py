import mido
import scheduler


port = mido.open_output("IAC Driver IAC Bus 1")
print(port)


class SequenceEventHandler:
    def high_priority(self, event):
        pass

    def low_priority(self, event):
        pass

    def pre_calc(self, event, current_time):
        event.calc_next_playback_time(current_time)


class DrumEventHandler(SequenceEventHandler):
    def __init__(self, nn, vel, ch, duration):
        self.nn = nn
        self.vel = vel
        self.ch = ch
        self.duration = duration

    def high_priority(self, event):
        port.send(mido.Message('note_on', note=self.nn, velocity=self.vel, channel=self.ch))
        print("DRUM EVENT:", self.nn, self.vel, self.ch, self.duration)

    def low_priority(self, event):
        note_off_time = event.next_playback_time + self.duration
        scheduler.add_event(note_off_time,
                            port.send, [mido.Message('note_off', note=self.nn, velocity=0, channel=self.ch)], {},
                            flush=False)


class DrumVelCycleEventHandler(SequenceEventHandler):
    def __init__(self, nn, vel, ch, duration):
        self.nn = nn
        self.vel = vel
        self.ch = ch
        self.duration = duration

        self.velocity_generator = self.get_next_vel()

    def high_priority(self, event):
        vel = next(self.velocity_generator)
        port.send(mido.Message('note_on', note=self.nn, velocity=vel, channel=self.ch))
        print("DRUM EVENT:", self.nn, self.vel, self.ch, self.duration)

    def low_priority(self, event):
        note_off_time = event.next_playback_time + self.duration
        scheduler.add_event(note_off_time,
                            port.send, [mido.Message('note_off', note=self.nn, velocity=0, channel=self.ch)], {},
                            flush=False)

    def get_next_vel(self):
        length = len(self.vel)
        i = 0
        while True:
            yield self.vel[i]
            i = (i + 1) % length