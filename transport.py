from time import monotonic


class Transport:
    def __init__(self, bpm=120, tpqn=480):
        self.bpm = bpm
        self.tpqn = tpqn # ticks per quarter note

        self.__running = False
        self.__start_time_s = 0
        self.__elapsed_time_s = 0

    def goto(self, time_s):
        self.__elapsed_time_s = time_s
        self.__start_time_s = time_s

    def start(self):
        tmp = self.__elapsed_time_s
        self.__start_time_s = monotonic()
        self.__running = True
        return tmp

    def stop(self):
        self.__elapsed_time_s += monotonic() - self.__start_time_s
        self.__running = False
        return self.__elapsed_time_s

    def get_elapsed_ticks(self):
        return self.convert_seconds_to_ticks(self.get_elapsed_s())

    def get_elapsed_s(self):
        if self.__running:
            return self.__elapsed_time_s + monotonic() - self.__start_time_s
        else:
            return self.__elapsed_time_s

    def convert_seconds_to_ticks(self, seconds):
        return seconds * self.get_ticks_per_second()

    def get_ticks_per_second(self):
        return self.bpm * self.tpqn / 60

    def is_running(self):
        return self.__running

    def debug_print(self):
        print(f"    running: {self.__running}")
        print(f"    start_time_s: {self.__start_time_s}")
        print(f"    elapsed_time_s: {self.get_elapsed_s()}")
        print(f"    elapsed_time_ticks: {self.get_elapsed_ticks()}")


if __name__ == '__main__':
    from time import sleep

    t = Transport()
    print("BEFORE interval 1")
    t.debug_print()
    t.start()
    sleep(1)
    print("DURING interval 1")
    t.debug_print()
    sleep(0.5)
    t.stop()
    print("AFTER interval 1")
    t.debug_print()
