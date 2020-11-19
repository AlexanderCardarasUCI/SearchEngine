import timeit

class StopWatch:
    def __init__(self):
        self.start = 0
        self.stop = 0

    def start_timer(self):
        self.start = timeit.default_timer()

    def stop_timer(self):
        self.stop = timeit.default_timer()

    def duration(self):
        return self.stop - self.start
