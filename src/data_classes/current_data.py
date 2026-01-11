import threading
from .threadsafe_list import ThreadSafeList
from .daa_spec import DaaSpec
from daamsim.Config import Configuration
import json
import numpy as np
import pickle

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
                setattr(self, name, np.array([]))
            self._initialized = True
            self._sim_state = 0
            self.specs = Configuration.get_instance().daa_spec

    def clear(self):
        del self
    
    def toJSON(self):
        dictionary = dict()
        dictionary['JSONIdentifier'] = "DAAMSIMJSON"
        dictionary['_initialized'] = self._initialized
        dictionary['_sim_state'] = self._sim_state
        dictionary['specs'] = self.specs
        for name in self._fields_names:
            dictionary[name] = getattr(self, name)

        return json.dumps(pickle.dumps(dictionary).decode("latin-1"), indent= 4)
    

    
    def fromJSON(self, json_string) -> bool: 
        self.clear()
        dictionary: dict = pickle.loads(json.loads(json_string).encode("latin-1"))
        if dictionary['JSONIdentifier'] != "DAAMSIMJSON":
            return False
        
        # self._initialized = dictionary["_initialized"]
        # self._sim_state = dictionary["_sim_state"]
        # self.specs.fromJSON(dictionary["specs"])
        
        dictionary.pop('JSONIdentifier')
        # dictionary.pop("_initialized")
        # dictionary.pop("_sim_state")
        
        for name in dictionary.keys():
            setattr(self, name, dictionary[name])
   
        return True
        
