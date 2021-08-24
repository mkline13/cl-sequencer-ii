import transport, midi

t = transport.Transport(bpm=120, tpqn=480)
sequences = []
running = False


midi_map = {
    "k": 36,
    "s": 39,
    "h": 42,
}


def play():
    global running

    # setup
    current_time = t.get_elapsed_ticks()
    for s in sequences:
        s.calc_all_playback_times(current_time)

    # playback loop
    running = True
    t.start()
    while running:
        current_time = t.get_elapsed_ticks()

        current_events = []

        for s in sequences:
            for e in s.get_current_events(current_time):
                current_events.append(e)

        for e in current_events:
            play_event(e)

        for s in sequences:
            s.recalc_played_events(current_time)

        if t.get_elapsed_ticks() > 10000:
            stop()


def stop():
    global running
    running = False


def play_event(event):
    if event.code in midi_map.keys():
        midi.note_on(midi_map[event.code], 127, 1)
    #print("PLAYING", event)


if __name__ == '__main__':
    import sequence
    sequences.append(sequence.Sequence.new_from_string("ksks", t.tpqn))
    sequences.append(sequence.Sequence.new_from_string("h", t.tpqn / 5))
    sequences.append(sequence.Sequence.new_from_string("   k", t.tpqn / 5))
    for s in sequences:
        print("SEQ>>>", s.input_string, '    grid:', s.tpb)
    play()