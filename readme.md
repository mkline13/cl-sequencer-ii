IT"S ALIVE!!!

INSTRUCTIONS:
- Run from 'app.py'.
- Enter '/help' for tutorial
- change the midi device by editing 'midi.py'
- sequencer code mappings are in 'output.py' in the EventHandler class and above functions

---

TODO:
- refactor event handling + command binding to use a decorator syntax for general hotness
- refactor the Event handling to be simpler and more fun
- implement more user commands for fun and profit
- rethink error handling
- rebuild parser with new error handling system, go back to functional style
- add config file for setting up midi / bindings

DONE:
- mvp complete: I have a fully functional sequencer that can be easily extended

FOR THE FUTURE:
- maybe get rid of keyword args? Maybe not, they are good for things like probability '%22'
- change syntax for ergonomics?
  - make kwargs look like this: '%22', 'v100', 'n32' rather than with a colon
  - maybe make events like this: 'k(n32 v22 %11)' 's(11 v33)'
  - maybe use square brackets? 'k[22 @45 %66]s[11]b[%1]'
- figure out how to do fancy things in command line like inserting both parens with the open paren (like in a text editor)
- user-configurable event codes
- rewrite in C/C++? port to a microcontroller
