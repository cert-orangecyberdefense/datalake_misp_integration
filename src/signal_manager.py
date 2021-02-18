import signal


class SignalManager:
    """
    Listen to sigterm signal (via `kill -SIGTERM pid`) to toggle is_stop_requested
    """
    is_stop_requested = False

    def __init__(self):
        signal.signal(signal.SIGTERM, self.request_stop)

    def request_stop(self, signum, frame):
        self.is_stop_requested = True
