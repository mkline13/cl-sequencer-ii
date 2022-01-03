from threading import Lock, Thread

mediator_lock = Lock()


class Cmd:
    def __init__(self, command_name, cli_bindings, callback):
        self.command_name = command_name
        self.cli_bindings = cli_bindings
        self.callback = callback


class Mediator:
    def __init__(self, app):
        self.app = app

        # mapping of command names -> callback funcs
        self.commands = {}

        # mapping of cli commands -> callback funcs
        self.bindings = {}

        # command list for /help command
        self.help_list = []

        # This is the list of commands that will be available during runtime
        # user cli commands
        self.add_cmd("help", self.cmd_help, "/help", "/h")
        self.add_cmd("quit", self.cmd_quit, "/quit")
        self.add_cmd("start", self.cmd_start, "/go", "/g")
        self.add_cmd("stop", self.cmd_stop, "/stop", "/s")
        self.add_cmd("pause", self.cmd_pause, "/pause", "/p")
        self.add_cmd("list", self.cmd_list_sequences, "/list", "/l")
        self.add_cmd("delete-all", self.cmd_clear_sequences, "/delete-all", "/da")
        self.add_cmd("new_sequence", self.cmd_new_sequence, "/ns")

        # future commands
        self.add_cmd("subdivision", self.cmd_stub, "/subdiv", "/div")  # default subdivision for new sequences
        self.add_cmd("store", self.cmd_stub, "/store", "/s")  # stores seq in quick store '/s' OR in slots [0-x] '/s 3 4'
        self.add_cmd("recall", self.cmd_stub, "/recall", "/r")  # recalls seq in quick store '/r' OR in slot [0-x] '/r 3'
        self.add_cmd("delete", self.cmd_stub, "/delete", "/d")  # delete individual tracks '/delete 1 3'
        self.add_cmd("tempo", self.cmd_stub, "/bpm")  # jump to new tempo '/bpm 125'
        self.add_cmd("mute", self.cmd_stub, "/mute", "/m")  # mute all tracks '/mute' OR specific tracks '/mute 0 2'
        self.add_cmd("unmute", self.cmd_stub, "/unmute", "/um")  # unmute all tracks '/um' OR specific tracks '/um 3 4'
        self.add_cmd("toggle-mutes", self.cmd_stub, "/tmute", "/tm")  # toggle the mutes of all OR specific tracks

        # idea: quick mode
        # user can enter mode in which they can issue commands without typing '/'
        # good for dj-style control of sequencer
        self.add_cmd("quick-mode", self.cmd_stub, "/quick")

    def add_cmd(self, cmd_name, callback, *cli_bindings):
        # add command
        self.commands[cmd_name] = callback

        if cli_bindings:
            # add bindings
            for i in cli_bindings:
                self.bindings[i] = callback

            # add /help entry
            col1 = ', '.join(cli_bindings)
            col2 = str(callback.__doc__).strip()
            entry = (col1, col2)
            self.help_list.append(entry)

    def cli_command(self, cmd, args):
        success, message = self.bindings.get(cmd, self.cmd_no)(cmd, args)
        return success, message

    def command(self, cmd, args):
        success, message = self.commands.get(cmd, self.cmd_no)(cmd, args)
        return success, message

    def cmd_no(self, cmd, args):
        success = False
        message = [f"command '{cmd}' does not exist.  args: {args}"]
        return success, message

    def cmd_stub(self, cmd, args):
        """
        command stub that will be implemented later
        """
        success = False
        message = [f"command '{cmd}' not implemented yet.  args: {args}"]
        return success, message

    def cmd_quit(self, cmd, args):
        """
        quit the program
        """
        success = True
        message = ["quitting..."]
        return success, message

    def cmd_help(self, cmd, args):
        """
        get list of all available commands
        """
        col1_width = 16

        message = ["(commands)".ljust(col1_width) + "(description)"]
        for col1, col2 in self.help_list:
            message.append(f"{col1.ljust(col1_width)}{col2}")

        message.append('')
        message.append(f"tutorial:")
        message.append(f"  1. type in 'ksks' and hit enter to add a sequence")
        message.append(f"  2. type in '/start' to begin playback")
        message.append(f"  3. type in 'h' to add another sequence")
        message.append(f"  4. enjoy your creation :)")

        success = True
        return success, message

    def cmd_new_sequence(self, cmd, args):
        # TODO: use args for changing the subdivision for the particular sequence (division of tpqn)
        # format sequencer code
        seq_code = args[0]
        # send to the sequencer
        success, message = self.app.player.sequencer.new_sequence(seq_code)
        return success, message

    def cmd_list_sequences(self, cmd, args):
        """
        list all sequences
        """
        sequence_list = [f"{i}: '{s}'" for i, s in enumerate(self.app.player.sequencer.get_sequence_list())]
        if sequence_list:
            message = [f"sequences: {len(sequence_list)}"] + sequence_list
        else:
            message = ["sequences: <empty>"]

        success = True
        return success, message

    def cmd_clear_sequences(self, cmd, args):
        """
        clear all sequences
        """
        self.app.player.sequencer.sequences.clear()
        return True, ["cleared all sequences"]

    def cmd_start(self, cmd, args):
        """
        start playback
        """
        success, start_time = self.app.player.start()

        if success:
            message = [f"playback started at {start_time}s"]
        else:
            message = ["cannot start, already playing"]
        return success, message

    def cmd_stop(self, cmd, args):
        """
        stop playback and rewind
        """
        success, stop_time = self.app.player.stop()
        self.app.transport.goto(0)

        if success:
            message = [f"stopped at {round(stop_time, 2)}s and returned playhead to beginning"]
        else:
            message = [f"cannot stop, player is not running"]
        return success, message

    def cmd_pause(self, cmd, args):
        """
        pause playback
        """
        success, stop_time = self.app.player.stop()
        if success:
            message = [f"paused at {round(stop_time, 2)}s"]
        else:
            message = [f"cannot pause, player is not running"]
        return success, message

