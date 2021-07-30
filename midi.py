import sched
import time

import mido

s = sched.scheduler(time.time, time.sleep)
port = mido.open_output("IAC Driver IAC Bus 1")
print(port)


def note_on(nn, vel, ch):
    port.send(mido.Message('note_on', note=nn, velocity=vel, channel=ch))


def note_off(nn, ch):
    port.send(mido.Message('note_off', note=nn, velocity=0, channel=ch))


def note_with_length(nn, vel, ch, length):
    note_on(nn, vel, ch)
    s.enter(length, 1, note_off, [nn, ch])
    s.run(blocking=True)


if __name__ == '__main__':
    note_with_length(60, 127, 0, 0.1)
    note_with_length(48, 127, 0, 0.5)