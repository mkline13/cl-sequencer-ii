# cl-sequencer-ii

A midi sequencer with a command-line interface. Implements a custom language for defining musical sequences.

## Instructions:
- Run from 'app.py'.
- Enter '/help' for tutorial
- change the midi device by editing 'midi.py'
- sequencer code mappings are in 'events.py'

---

## Project status:
- mvp complete: I have a fully functional sequencer that can be easily extended

## Todo:
- implement note-offs with the scheduler
- implement more user commands for fun and profit

## Future ideas:
- implement cool note-generation event handlers using the scheduler (flurry, arpeggio, etc)
- change syntax for ergonomics?
  - maybe use spaces like this: 'k(n32 v22 %11)' 's(11 v33)'
  - maybe use square brackets? 'k[22 @45 %66]s[11]b[%1]'
- figure out how to do fancy things in command line like inserting both parens with the open paren (like in a text editor)
- user-configurable event codes
- rewrite in C/C++? port to a microcontroller
