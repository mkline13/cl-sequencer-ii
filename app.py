from cli import CLI
from mediator import Mediator
from player import Player
from transport import Transport


debug = False

class App:
    def __init__(self):
        # instantiate all application parts
        self.transport = Transport()
        self.player = Player(self.transport)
        self.mediator = Mediator(self)
        self.cli = CLI(self.mediator)

        # make any necessary connections between them
        self.playback_thread = None

    def run(self):
        # launch cli repl
        self.cli.boot_message()

        if debug:
            self.mediator.command("new_sequence", ["ksks"])
            self.mediator.command("go", [])

        quitting = 0
        while not quitting:
            quitting = self.cli.get_user_input()


if __name__ == '__main__':
    app = App()
    app.run()
