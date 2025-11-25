import threading
from .threadsafe_list import ThreadSafeList

class CurrentData:
    _instance = None
    _lock = threading.Lock()

    _fields_names = [
        "rr_val",
        "azimuth_vect",
        "r_min_m",
        "r_min_over",
        "ground_int_speed",
        "alpha_oncoming_vect",
        "alpha_overtake_vect",
        "clos_vel",
        "clos_vel_over",
        "specs",
    ]
    #0 for start up state
    #1 for rr_calcs ran
    _sim_state = 0

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
            self._sim_state = 0

    def clear(self):
        del self

