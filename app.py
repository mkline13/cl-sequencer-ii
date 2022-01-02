import player
from sequence import Sequence
import threading


repl_lock = threading.Lock()

class App:
    def __init__(self):
        self.commands = {
            "/help": self.api_print_help,
            "/start": self.api_start_player,
            "/stop": self.api_stop_player,
            "/clear": self.api_clear_all_sequences,
        }

        self.player = player.Player()

        self.tpb = 120 #current ticks per beat

        self.__playback_thread = threading.Thread(target=self.player.play)

    def repl_loop(self):
        # start REPL
        print()
        print("======= CLSEQUENCER ========")
        print("Type '/help' to get started.")
        print("============================")
        while True:
            # get user input
            user_input = input(">> ")

            # format and validate input
            user_input = user_input.strip().split(" ")

            if user_input[0] in self.commands:
                # handle '/' commands
                self.commands[user_input[0]](user_input[1:])
            else:
                self.api_add_sequence(user_input[0])
                # try to add input as sequence

    def api_print_help(self, cmd_args):
        print("type '/start' and then enter a sequence code (e.g. 'kkssksks')")
        print("commands:")
        for k, v in self.commands.items():
            print(f"  {k}")

    def api_start_player(self, cmd_args):
        """
        TODO: make thread start at beginning of program, maybe make an event feed that can be locked and accessed for messaging between threads

        """
        if not self.player.is_running:
            self.__playback_thread.start()

    def api_stop_player(self, cmd_args):
        if self.player.is_running:
            self.player.stop()

    def api_add_sequence(self, sequence_code):
        self.player.add_sequence(Sequence(sequence_code, self.tpb))

    def api_remove_sequence(self):
        pass

    def api_clear_all_sequences(self):
        self.player.clear_sequences()


if __name__ == '__main__':
    app = App()
    app.repl_loop()