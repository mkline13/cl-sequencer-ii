import midi
import random
from helpers import register


def midi_clamp(val):
    return max(0, min(127, int(val)))


output_mappings = {}


@register('drum', output_mappings)
def drum(scheduler, e):
    note = midi_clamp(e.params['n'])
    velocity = midi_clamp(e.params['v'] - random.randint(0, e.params['rv']))
    channel = midi_clamp(e.params['c'])

    if random.random() <= e.params['%']:
        midi.note_on(note, velocity, channel)

        # create the callback for the note off event in the scheduler
        def note_off_callback():
            midi.note_off(note, channel)

        # schedule the note off


@register('rest', output_mappings)
def rest(scheduler, e):
    pass



