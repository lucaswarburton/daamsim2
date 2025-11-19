import threading
from threadsafe_list import ThreadSafeList

class CurrentData:
    _instance = None
    _lock = threading.Lock()

    _fields_names = [
        "rr_val",
        "azimuth_vect",
        "r_min_m",
        "r_min_over",
        "alpha_oncoming_vect",
        "alpha_overtake_vect",
        "clos_vel",
        "clos_vel_over",
        "rtas_specs"
    ]

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            for name in self._fields_names:
                setattr(self, name, ThreadSafeList())
            self._initialized = True

    def clear(self):
        del self

