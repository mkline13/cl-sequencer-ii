from parser import parse, SeqParserError
from sequence import Sequence
from threading import Lock, Thread
from output import EventHandler

playback_lock = Lock()


class Sequencer:
    def __init__(self):
        self.sequences = []

    def new_sequence(self, seq_code, tpb=280):
        # try to parse the sequence
        try:
            parsed = parse(seq_code)
        except SeqParserError as e:
            success = False
            message = [f"invalid sequence code: '{seq_code}'", f"reason: {str(e)}"]
            return success, message

        sequence = Sequence(seq_code, parsed, tpb)
        self.sequences.append(sequence)

        success = True
        message = [f"added new sequence: {seq_code}"]
        return success, message

    def get_sequence_list(self):
        return [s.input_string for s in self.sequences]


class Scheduler:
    def __init__(self):
        # TODO: implement scheduler
        self.events = []


class Player:
    def __init__(self, transport):
        # links
        self.transport = transport

        # components
        self.sequencer = Sequencer()
        self.scheduler = Scheduler()
        self.event_handler = EventHandler(self)

        # playback variables
        self.__running = False
        self.__previous_time = 0
        self.__playback_thread = None

    def start(self):
        with playback_lock:
            running = self.__running

        if not running:
            start_time = self.transport.get_elapsed_s()
            self.__previous_time = start_time - 10
            self.__playback_thread = Thread(target=self.playback_loop, daemon=True)
            self.__playback_thread.start()
            return True, start_time
        else:
            return False, None

    def stop(self):
        with playback_lock:
            running = self.__running

        if running:
            with playback_lock:
                self.__running = False
            self.__playback_thread.join()
            success = True
            stop_time = self.transport.get_elapsed_s()
        else:
            success = False
            stop_time = None

        return success, stop_time

    def playback_loop(self):
        with playback_lock:
            self.__running = True
            self.transport.start()

        while self.__running:
            with playback_lock:
                self.step()

        with playback_lock:
            self.transport.stop()

    def step(self):
        current_time = self.transport.get_elapsed_ticks()

        played = set()  # store a set of played event codes so that duplicate notes are not played

        # trigger events contained in sequence
        for sequence in self.sequencer.sequences:
            # uses a 1D collision algorithm to determine if notes should be played
            # calculate event collision range
            collision_interval = current_time - self.__previous_time
            low = self.__previous_time % sequence.length
            high = low + collision_interval

            # loop through all events and check if they are in the collision range
            for event in sequence.events:
                if event.play_time > high:
                    continue
                elif event.code in played:
                    continue
                elif low < event.play_time or low - sequence.length < event.play_time <= high - sequence.length:
                    # handle normal notes OR notes that occur when the loop cycles back to the beginning
                    self.event_handler.dispatch(event)
                    played.add(event.code) # mark the event code as played so duplicates are not played

        # TODO: trigger events in scheduler

        # prepare for next step
        self.__previous_time = current_time
        played.clear()
