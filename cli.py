

class CLI:
    def __init__(self, mediator):
        self.mediator = mediator
        self.prompt = ">>  "
        self.info = "  ??  "
        self.error = "  !!  "

    def boot_message(self):
        print()
        print("======= CLSEQUENCER ========")
        print(self.info + "type '/help' to get started")
        print()

    def print_message(self, message, indent='      ', error=False):
        lines = (line for line in message)

        if error:
            print(self.error + next(lines))
        else:
            print(self.info + next(lines))

        for line in lines:
            print(indent + line)

    def get_user_input(self):
        # get input from the user
        raw_user_input = input(self.prompt)

        # format and validate input
        user_input = raw_user_input.strip().split(" ")

        if user_input[0] in ['', '/']:
            # return if blank
            return 0
        elif user_input[0][0] == "/":
            # if commands are NOT sequence codes
            cmd, cmd_args = user_input[0], user_input[1:]

            # send command to mediator
            success, message = self.mediator.command(cmd, cmd_args)

            # handle quitting
            if cmd == "/quit":
                self.print_message(message)
                return 1
        else:
            # handle sequence codes
            success, message = self.mediator.cmd_new_sequence("", user_input)

        if success:
            self.print_message(message)
        else:
            self.print_message(message, error=True)

        # application will quit when '1' is returned
        return 0
