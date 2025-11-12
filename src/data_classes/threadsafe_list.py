import threading

class ThreadSafeList:
    def __init__(self, initial=None):
        self._lock = threading.Lock()
        self._list = list(initial) if initial else []

    def append(self, value):
        with self._lock:
            self._list.append(value)

    def clear(self):
        with self._lock:
            self._list.clear()

    def get(self):
        with self._lock:
            return list(self._list)  # return a copy

    def set(self, new_list):
        with self._lock:
            self._list = list(new_list)

    def __len__(self):
        with self._lock:
            return len(self._list)

    def __getitem__(self, index):
        with self._lock:
            return self._list[index]

    def __iter__(self):
        with self._lock:
            return iter(list(self._list))  # copy for safe iteration
