class Alert():

    def __init__(self, state, message):
        self._state = state
        self._message = message

    @property
    def state(self):
        return self._state

    @property
    def message(self):
        return self._message
