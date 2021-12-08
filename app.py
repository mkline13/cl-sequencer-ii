import player
import sys


class App:
    def __init__(self):
        self.data = {}
        self.player = player.Player(app)

        self.commands = {
            "quit": self.quit,
        }

    def command(self, cmd_string, args, kwargs):
        if cmd_string in self.commands:
            self.commands[cmd_string](*args, **kwargs)
        else:
            print(f"No such command: '{cmd_string}'")

    def quit(self, *args, **kwargs):
        print("QUITTING!")
        sys.exit()
