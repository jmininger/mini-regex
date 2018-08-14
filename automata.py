class NFA:
    def __init__(self):
        self._states = {}
        self._start = 0

class NFA_Iterator:
    def __init__(self):
        self._current = 0

class NFA_Session:
    def __init__(self):
        self._states = set()
    def add_state(self, iter):
        self._current.add(iter)
    def 
