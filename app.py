import player
import sys


class App:
    def __init__(self):
        self.data = {}
        self.player = player.Player(app)

        self.commands = {
            "quit": (self.quit, [], {}),
        }

    def command(self, cmd_string):
        if cmd_string in self.commands:
            func, args, kwargs = self.commands[cmd_string]
            func(*args, **kwargs)
        else:
            print(f"No such command: '{cmd_string}'")

    def quit(self, *args, **kwargs):
        print("QUITTING!")
        sys.exit()
