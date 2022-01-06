
def add_bindings(*bindings):
    """
    A decorator function that associates functions with strings that will be used as commands in the cli.
    """
    def decorator(func):
        func.cmd_bindings = bindings
        return func
    return decorator


class Mediator:
    def __init__(self, app):
        self.app = app

        self.commands = {}
        self.help_list = []

        # search for commands bound with '@add_binding' and add to the command dict and help list
        for name in dir(Mediator):
            member = getattr(Mediator, name)
            if hasattr(member, 'cmd_bindings'):
                # variable renamed for clarity
                func = member
                # add to the commands dict
                for b in func.cmd_bindings:
                    self.commands[b] = func
                # add to the help list
                col1 = ', '.join(func.cmd_bindings)
                col2 = str(func.__doc__).strip()
                entry = (col1, col2)
                self.help_list.append(entry)

        # future commands
        """
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
        """

    def command(self, cmd, cmd_args):
        if cmd in self.commands:
            func = self.commands[cmd]
            success, message = func(self, cmd, cmd_args)
            return success, message
        else:
            success, message = self.cmd_nonexistent(cmd, cmd_args)
            return success, message

    def cmd_nonexistent(self, cmd, cmd_args):
        """
        called when a command doesn't exist
        """
        return False, [f"command '{cmd}' does not exist."]

    @add_bindings('/quit')
    def cmd_quit(self, cmd, cmd_args):
        """
        quit the program
        """
        return True, ["quitting..."]

    @add_bindings('/h', '/help')
    def cmd_help(self, cmd, cmd_args):
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
        message.append(f"  5. parameters can be added to events like this: 'ks(~v100)k(%0.6)s(n50)'")
        message.append(f"  6. TODO: add a way for the user to query usable parameters") #TODO

        return True, message

    def cmd_new_sequence(self, cmd, cmd_args):
        # TODO: use cmd_args for changing the subdivision for the particular sequence (division of tpqn)
        # format sequencer code
        seq_code = cmd_args[0]
        # send to the sequencer
        success, message = self.app.player.sequence_manager.new_sequence(seq_code)
        return success, message

    @add_bindings('/ls')
    def cmd_list_sequences(self, cmd, cmd_args):
        """
        list all sequences
        """
        sequence_list = [f"{i}: '{s}'" for i, s in enumerate(self.app.player.sequence_manager.get_sequence_list())]
        if sequence_list:
            message = [f"sequences: {len(sequence_list)}"] + sequence_list
        else:
            message = ["sequences: <empty>"]
        return True, message

    @add_bindings('/clear')
    def cmd_clear_sequences(self, cmd, cmd_args):
        """
        clear all sequences
        """
        self.app.player.sequence_manager.sequences.clear()
        return True, ["cleared all sequences"]

    @add_bindings('/start', '/go', '/g')
    def cmd_start(self, cmd, cmd_args):
        """
        start playback
        """
        success, start_time = self.app.player.start()

        if success:
            message = [f"playback started at {start_time}s"]
        else:
            message = ["cannot start, already playing"]
        return success, message

    @add_bindings('/stop', '/s')
    def cmd_stop(self, cmd, cmd_args):
        """
        stop playback and rewind
        """
        success, stop_time = self.app.player.stop()
        self.app.transport.goto(0)

        if success:
            message = [f"stopped at {round(stop_time, 2)}s and returned playhead to start"]
        else:
            message = [f"cannot stop, player is not running"]
        return success, message

    @add_bindings('/pause')
    def cmd_pause(self, cmd, cmd_args):
        """
        pause playback
        """
        success, stop_time = self.app.player.stop()
        if success:
            message = [f"paused at {round(stop_time, 2)}s"]
        else:
            message = [f"cannot pause, player is not running"]
        return success, message

