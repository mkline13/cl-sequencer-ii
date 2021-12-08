from sequence import Sequence
from transport import Transport
import output


class EventDispatch:
    def __init__(self):
        self.mapping = {
            "k": self.kick,
            "b": self.block,
            "s": self.snare,
            "h": self.hat,
            ".": self.rest,
            "w": self.print,
        }

    def dispatch(self, event):
        self.mapping[event.code](event)

    def rest(self, event):
        pass

    def kick(self, event):
        # defaults
        params = {
            "vel": 100,
            "rvel": 0,
            "prob": 1
        }

        # ordered args
        for param_name, arg in zip(["vel", "rvel", "prob"], event.args):
            params[param_name] = arg

        # kwargs
        params.update(event.kwargs)

        # send output
        output.drum(36, params["vel"], params["rvel"], params["prob"], 1)

    def snare(self, event):
        # defaults
        params = {
            "vel": 100,
            "rvel": 0,
            "prob": 1
        }

        # ordered args
        for param_name, arg in zip(["vel", "rvel", "prob"], event.args):
            params[param_name] = arg

        # kwargs
        params.update(event.kwargs)

        # send output
        output.drum(38, params["vel"], params["rvel"], params["prob"], 1)

    def hat(self, event):
        # defaults
        params = {
            "vel": 100,
            "rvel": 0,
            "prob": 1
        }

        # ordered args
        for param_name, arg in zip(["vel", "rvel", "prob"], event.args):
            params[param_name] = arg

        # kwargs
        params.update(event.kwargs)

        # send output
        output.drum(42, params["vel"], params["rvel"], params["prob"], 1)

    def block(self, event):
        # defaults
        params = {
            "vel": 100,
            "rvel": 50,
            "prob": 0.5
        }

        # ordered args
        for param_name, arg in zip(["vel", "rvel", "prob"], event.args):
            params[param_name] = arg

        # kwargs
        params.update(event.kwargs)

        # send output
        output.drum(37, params["vel"], params["rvel"], params["prob"], 1)

    def print(self, event):
        print("PLAYING:", event.code)


class Player:
    def __init__(self):
        self.dispatch = EventDispatch()
        self.transport = Transport(bpm=120, tpqn=480)
        self.__sequences = []
        self.__running = False

    def add_sequence(self, sequence):
        self.__sequences.append(sequence)

    def play(self):
        for s in self.__sequences:
            s.print()

        previous_time = -10

        # prevents playing the same note more than once at a time
        played = set()

        self.__running = True
        print("player running...")

        self.transport.start()

        while self.__running:
            current_time = self.transport.get_elapsed_ticks()

            for sequence in self.__sequences:
                # calculate event collision range
                collision_interval = current_time - previous_time
                low = previous_time % sequence.length
                high = low + collision_interval

                # print("check", current_time, low, high)

                for event in sequence.events:
                    if event.play_time > high:
                        continue
                    elif event.code in played:
                        continue
                    elif low < event.play_time or low - sequence.length < event.play_time <= high - sequence.length:
                        # handle normal notes OR notes that occur when the loop cycles back to the beginning
                        self.dispatch.dispatch(event)
                        played.add(event.code) # mark the note as played so that it isn't played again this time
                        # print("BLAMO", current_time, event.code)

            previous_time = current_time
            played.clear()

            ## AUTO STOP FOR TESTING
            # if current_time > 2000: self.stop()

        print("stopped...")

    def stop(self):
        self.transport.stop()
        self.__running = False


if __name__ == '__main__':
    tpqn = 480
    p = Player()
    p.add_sequence(Sequence("k", tpqn))
    p.add_sequence(Sequence(".s", tpqn))
    p.add_sequence(Sequence(".k(90, 80).", tpqn / 4))
    p.add_sequence(Sequence(".h(50)h(50)h(50)", tpqn / 4))
    p.add_sequence(Sequence("b..", tpqn / 4))
    p.play()