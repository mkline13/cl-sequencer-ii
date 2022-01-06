import midi
import random
from helpers import register


def midi_clamp(val):
    return max(0, min(127, int(val)))


output_mappings = {}


@register('drum', output_mappings)
def drum(scheduler, note=32, vel=127, chan=1, rand_vel=0, prob=1.0, length=100):
    note = midi_clamp(note)
    vel = midi_clamp(vel - random.randint(0, rand_vel))
    chan = midi_clamp(chan)

    if random.random() <= prob:
        midi.note_on(note, vel, chan)

        # create the callback for the note off event in the scheduler
        def note_off_callback():
            midi.note_off(note, chan)

        # schedule the note off


@register('rest', output_mappings)
def rest(scheduler, e):
    pass



