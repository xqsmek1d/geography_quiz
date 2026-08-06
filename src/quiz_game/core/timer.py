import time

class Timer:

    def __init__(self, duration: int | None):
        self.duration = duration
        self.start_time = None

    def start(self):

        self.start_time = time.monotonic()

    @property
    def elapsed(self) -> int | None:
        
        if self.start_time is None:
            return 0

        return int(time.monotonic() - self.start_time)

    @property
    def remaining(self) -> int | None:

        if self.duration is None:
            return None

        remaining = (self.duration - (time.monotonic() - self.start_time))

        return max(0, int(remaining),)

    @property
    def expired(self) -> bool:

        if self.duration is None:
            return None

        return self.remaining <= 0

class GameTimer(Timer):
    def __init__(self, duration: int | None):
        super().__init__(duration)

class QuestionTimer(Timer):
    def __init__(self, duration: int | None):
        super().__init__(duration)