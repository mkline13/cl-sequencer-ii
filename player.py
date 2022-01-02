from transport import Transport
import output
from threading import Lock


player_lock = Lock()


class Player:
    def __init__(self):
        self.dispatch = output.EventDispatch()
        self.transport = Transport(bpm=120, tpqn=480)
        self.scheduler = None
        self.__sequences = []
        self.__running = False

    def add_sequence(self, sequence):
        self.__sequences.append(sequence)

    def clear_sequences(self):
        self.__sequences = []

    def play(self):
        # for s in self.__sequences:
        #     s.print()
        with player_lock:
            previous_time = -10

            # prevents playing the same note more than once at a time
            played = set()

            self.__running = True
            print("player running...")

            self.transport.start()

        while self.__running:
            with player_lock:
                current_time = self.transport.get_elapsed_ticks()

                # trigger events contained in sequence
                for sequence in self.__sequences:
                    # uses a 1D collision algorithm to determine if notes should be played
                    # calculate event collision range
                    collision_interval = current_time - previous_time
                    low = previous_time % sequence.length
                    high = low + collision_interval

                    # loop through all events and check if they are in the collision range
                    for event in sequence.events:
                        if event.play_time > high:
                            continue
                        elif event.code in played:
                            continue
                        elif low < event.play_time or low - sequence.length < event.play_time <= high - sequence.length:
                            # handle normal notes OR notes that occur when the loop cycles back to the beginning
                            self.dispatch.dispatch(event, self.scheduler)
                            played.add(event.code) # mark the note as played so that it isn't played again this time
                            # print("BLAMO", current_time, event.code)

                # trigger events in scheduler

                # prepare for next cycle
                previous_time = current_time
                played.clear()

            ## AUTO STOP FOR TESTING
            # if current_time > 2000: self.stop()

        # print("stopped...")

    def stop(self):
        with player_lock:
            self.transport.stop()
            self.__running = False

    @property
    def is_running(self):
        return self.__running


if __name__ == '__main__':
    from sequence import Sequence
    tpqn = 480
    p = Player()
    p.add_sequence(Sequence("k", tpqn))
    p.add_sequence(Sequence(".s", tpqn))
    p.add_sequence(Sequence(".k(90, 80).", tpqn / 4))
    p.add_sequence(Sequence(".h(50)h(50)h(50)", tpqn / 4))
    p.add_sequence(Sequence("b..", tpqn / 4))
    p.play()