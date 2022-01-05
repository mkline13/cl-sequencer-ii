from parser import parse, SeqParserError
from sequence import Sequence
from threading import Lock, Thread
from events import sequencer_event_bindings
from output import output_mappings


class SequenceManager:
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

        # convert the parsed sequence into events
        events = []
        for i, (code, args, kwargs) in enumerate(parsed):
            # todo: report errors when there is an unbound sequencer code
            e = sequencer_event_bindings.get(code, '.')(code, args, kwargs, i * tpb)
            events.append(e)

        self.sequences.append(Sequence(seq_code, events, tpb))

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
        self.sequence_manager = SequenceManager()
        self.scheduler = Scheduler()

        # playback variables
        self.__running = False
        self.__previous_time = 0
        self.__playback_thread = None
        self.__lock = Lock()

    def start(self):
        with self.__lock:
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
        with self.__lock:
            if self.__running:
                self.__running = False
            else:
                return False, None

        self.__playback_thread.join()  # not in lock to prevent deadlock (?)
        return True, self.transport.get_elapsed_s()

    def playback_loop(self):
        with self.__lock:
            self.__running = True
            self.transport.start()

        while self.__running:
            with self.__lock:
                self.step()

        with self.__lock:
            self.transport.stop()

    def step(self):
        current_time = self.transport.get_elapsed_ticks()

        played = set()  # store a set of played event codes so that duplicate notes are not played

        # trigger events contained in sequence
        for sequence in self.sequence_manager.sequences:
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
                    # get output handler
                    handler = output_mappings[event.output]
                    handler(self.scheduler, event)
                    # mark the event code as played so duplicates are not played
                    played.add(event.code)

        # TODO: trigger events in scheduler

        # prepare for next step
        self.__previous_time = current_time
        played.clear()
