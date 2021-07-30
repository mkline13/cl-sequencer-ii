from time import sleep

from parser import parse
from sequence_event_handler import handle_event
import signal


from transport import Transport


class Application:
    def __init__(self):
        self.transport = Transport()
        signal.register("transport.start", print)
        signal.register("transport.stop", print)

    def load(self):
        sequences = [
            parse("skk(-10.100, 20, j:33) k(55, 22, %bab:505, v:100)s"),
            parse("ks ks ksk"),
            parse("k(100,100,100)s     ")
        ]
        print("LOADED: ", sequences)
        return sequences

    def run(self):
        sequence = self.load()[0]
        app.transport.start()
        for i in sequence:
            handle_event(i)
            sleep(0.2)
        app.transport.stop()


if __name__ == '__main__':
    app = Application()
    app.run()