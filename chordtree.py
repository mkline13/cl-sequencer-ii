#!/usr/bin/env python
# coding: utf-8

# In[80]:

import mido
import time
import random


class ChordNode:
    def __init__(self, *notes):
        self.notes = list(notes)
        self.children = []

    def add_child(self, *notes):
        child = ChordNode(*notes)
        self.children.append(child)
        return child

    def __repr__(self):
        tmp = [str(n) for n in self.notes]
        return f"ChordNode({', '.join(tmp)})"


# In[81]:


def df_traverse(node, gen=0):
    yield node, gen
    for c in node.children:
        yield from df_traverse(c, gen+1)


def print_tree(node):
    for n, g in df_traverse(node):
        indent = g * "  "
        print(indent + str(n.notes))


# In[95]:


def octave_wrap_notes(notes):
    return [n % 12 for n in notes]


# In[105]:


def build_chord_tree(chord_node, memo=set(), gens=4):
    if gens > 0:
        for anchor in chord_node.notes:
            possibilities = []
            possibilities.append([anchor, anchor + 5, anchor + 9])
            possibilities.append([anchor, anchor + 5, anchor + 10])
            possibilities.append([anchor, anchor + 1, anchor + 5])

        for p in possibilities:
            p = octave_wrap_notes(p)
            # if p != chord_node.notes and tuple(p) not in memo:
            if p != chord_node.notes:
                chord_node.add_child(*p)
                memo.add(tuple(p))

        for c in chord_node.children:
            build_chord_tree(c, memo, gens - 1)


port = mido.open_output("IAC Driver IAC Bus 1")
print(port)


def note_on(nn, vel, ch):
    port.send(mido.Message('note_on', note=nn, velocity=vel, channel=ch))


def note_off(nn, ch):
    port.send(mido.Message('note_off', note=nn, velocity=0, channel=ch))


def play_chord(chord):
    for n in chord:
        note_on(n, 127, 1)
    return chord


def stop_chord(chord):
    for n in chord:
        note_off(n, 1)


def play_progression(chords, octave = 48, delay=0.7):
    for i in chords:
        notes = [n + octave for n in i]
        print(notes)
        play_chord(notes)
        time.sleep(delay)
        stop_chord(notes)


def generate_progression(chord_tree, octave = 48, length=8):
    yield chord_tree.notes
    if length > 0 and len(chord_tree.children) > 0:
        yield from generate_progression(random.choice(chord_tree.children), length - 1)

# In[106]:

root = ChordNode(0, 4, 7)
build_chord_tree(root, gens=8)

prog1 = [i for i in generate_progression(root, length= 24)]
prog2 = [i for i in generate_progression(root)]
print(prog1)
print(prog2)

play_progression(prog1, 60)
# play_progression(prog2, 48, 0.5)


