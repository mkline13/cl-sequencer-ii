Sequencer works!

Run from 'player.py' and edit the sequences in the 'if __main__' section.


TODO:
- proper event handlers for played events
    - high priority funcs
    - low priority funcs
    - precalculation funcs
- build low-priority scheduler queue for note-offs and other things
- command line interface + separate threads for UI and playback

DONE:
- built parser
- built event player
- built sequence and event data structure

FOR THE FUTURE:
- user-configurable event codes