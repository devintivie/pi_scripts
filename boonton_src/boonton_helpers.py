import enum

def get_ctype_string(ctype_string):
    tmp = str(ctype_string.value, encoding='utf-8')
    return tmp

class boonton_trigger_mode(enum.Enum):
    normal = 1,
    auto_trig = 2
    auto_level = 3
    free_run = 4

class boonton_units(enum.Enum):
    dBm = 0
    watts = 1
    volts = 2
    dBV = 3
    dBmV = 4
    dBuV = 5

class collect_gate(object):
    def __init__(self, start, stop):
        self.start = float(start)
        self.stop = float(stop)