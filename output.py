import midi
import random


def drum(note, velocity, random_velocity, probability, channel):
    velocity -= random.randint(0, random_velocity)
    if random.random() <= probability:
        midi.note_on(note, int(velocity), int(channel))