"""Define CountTimer."""


import time
from math import inf


class CountTimer:
    """
    A counting timer, w/ optional expiry, that can be started, paused, resumed and reset.

    Configuration:
        duration: Number of seconds to elapse before expiration
                  (optional; default: 0 indicates time never expires)

    Methods:
        start(): start the timer
        pause(): pause the timer
        resume(): resume the timer
        set_start_time(minutes): set the start time manually in minutes
        reset(): reset the timer to default (duration 0/paused/not started)

    Properties:
        paused: True if timer is paused
        running: True if timer is running
        duration: value of the 'duration' config param
        elapsed: time (sec) since timer was started
        remaining: time (sec) until timer expires

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
        """Reset timer to new duration."""
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

    def set_start_time(self, minutes):
        """Set the start time manually in minutes."""
        self._time_started = time.time() - (minutes * 60)
        self._time_paused = time.time()
        self._paused = True

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
        """Return True if the timer is paused, False if not."""
        return self._paused

    @property
    def running(self) -> bool:
        """Return False if the timer is paused, True if not."""
        return not self._paused

    @property
    def duration(self) -> bool:
        """Timer's configured expiry value."""
        return self._duration

    @property
    def expired(self) -> bool:
        """Return True if the timer has expired, False if not."""
        return self.elapsed >= self._duration and self._duration != 0

    @property
    def elapsed(self) -> float:
        """Time (seconds) since timer was started, minus time paused."""
        got = self._get()
        return got or 0

    @property
    def remaining(self) -> float:
        """Time left (in seconds) until the timer expires."""
        got = self._get()
        time_left = self._duration - got if self._duration else inf
        return max(time_left, 0)
