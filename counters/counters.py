import time


class CountupTimer:
    """
    A counting-up timer that can be started, paused, resumed and reset.

    Configuration:
        duration: Time in seconds before timer expires

    Methods:
        Start: starts the timer
        Pause: pauses the timer
        Resume: resumes the timer
        Reset: Resets the timer to 0/paused/not started

    Properties:
        Elapsed: Time in seconds since timer was started
        Paused: True if timer is paused
        Running: True if timer is running
        Remaining: Time left in countup until timer expires

    Inspiration from https://stackoverflow.com/a/60027719/4402572
    """

    def __init__(self, duration=0):
        """Create a new timer."""
        self._time_started = None
        self._time_paused = None
        self._elapsed = 0
        self._paused = True
        self._duration = duration

    def reset(self, duration=0):
        self.__init__(duration)

    def start(self):
        """Start the timer."""
        if self._time_started:
            return
        self._time_started = time.time()
        self._paused = False

    def pause(self):
        """Pause the timer."""
        if self._paused or self._time_started is None:
            return
        self._time_paused = time.time()
        self._paused = True

    def resume(self):
        """Resume the timer."""
        if not self._paused or self._time_started is None:
            return
        pause_duration = time.time() - self._time_paused
        self._time_started = self._time_started + pause_duration
        self._paused = False

    def _get(self) -> float:
        """Time in sec since timer was started, minus any time paused."""
        if not self._time_started:
            return 0
        if self._paused:
            return self._time_paused - self._time_started
        else:
            return time.time() - self._time_started

    @property
    def paused(self) -> bool:
        """True if the timer is paused, False if not."""
        return self._paused

    @property
    def running(self) -> bool:
        """False if the timer is paused, True if not."""
        return not self._paused

    @property
    def elapsed(self) -> float:
        """Time elapsed (seconds) since timer was started, minus time paused."""
        got = self._get()
        return got or 0

    @property
    def duration(self) -> bool:
        """Timer's configured expiry value."""
        return self._duration

    @property
    def expired(self) -> bool:
        """True if the timer has expired, False if not."""
        return self.elapsed >= self._duration

    @property
    def remaining(self) -> float:
        """Time left (in seconds) until the timer expires."""
        got = self._get()
        time_left = self._duration - got
        return time_left if time_left <= self.duration else 0


class CountdownTimer(CountupTimer):
    """
    A timer that can be started, paused, resumed and reset.

    Configuration:
        duration: Time in seconds before timer expires

    Methods:
        Start: starts the timer
        Pause: pauses the timer
        Resume: resumes the timer
        Reset: Resets the timer to 0/paused/not started

    Properties:
        Elapsed: Time in seconds since timer was started
        Paused: True if timer is paused
        Running: True if timer is running
        Remaining: Time left in countdown until the timer expires

    Inspiration from https://stackoverflow.com/a/60027719/4402572
    """

    @property
    def remaining(self) -> float:
        """Time left (in seconds) until the timer expires."""
        got = self._get()
        time_left = self._duration - got
        return max(time_left, 0)
