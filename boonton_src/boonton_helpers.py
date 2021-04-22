import enum

def get_ctype_string(ctype_string):
    tmp = str(ctype_string.value, encoding='utf-8')
    return tmp

def get_error_msg(intValue):
    tmp = boonton_error_code(intValue).name
    return tmp

class boonton_trigger_mode(enum.Enum):
    normal = 1,
    auto_trig = 2
    auto_level = 3
    free_run = 4

class boonton_trigger_source(enum.Enum):
    channel1 = 0
    channel2 = 1
    external = 2
    channel3 = 3
    channel4 = 4
    channel5 = 5
    channel6 = 6
    channel7 = 7
    channel8 = 8
    channel9 = 9
    channel10 = 10
    channel11 = 11
    channel12 = 12
    channel13 = 13
    channel14 = 14
    channel15 = 15
    channel16 = 16
    independent = 17

class boonton_bandwidth(enum.Enum):
    high = 0
    low = 1

class boonton_units(enum.Enum):
    dBm = 0
    watts = 1
    volts = 2
    dBV = 3
    dBmV = 4
    dBuV = 5

class boonton_trigger_slope(enum.Enum):
    negative = 0
    positive = 1

class boonton_error_code(enum.Enum):
    io_general = -2147204588
    io_timeout = -2147204587
    model_not_supported = -2147204586
    invalid_parameter = 0xBFFF0078
    invalid_session_handle = 0x1190
    status_not_available = 0x005D
    error_reset_failed = 0x005F
    error_resource_unknown = 0x0060
    already_initialized = 0x0061
    out_of_memory = 0x0056
    operation_pending = 0x0057
    null_pointer = 0x0058
    unexpected_response = 0x0059
    not_initialzied = 0x001D
    libusb_io_error = -1
    libusb_invalid_parameter = -2
    lubusb_access_error = -3
    libusb_error_no_device = -4
    libusb_not_found = -5
    libusb_busy = -6
    libusb_timeout = -7
    libusb_overflow = -8
    libusb_pipe_error = -9
    libusb_interrupted = -10
    libusb_no_mem = -11
    libusb_not_supported = -12
    libusb_other_error = -99

    # def __str__(self):
    #     return self.string

class boonton_status(enum.Enum):
    not_initialized = 'Not Initialized'
    initialized = 'Initialized'
    closed = 'Closed'

class collect_gate(object):
    def __init__(self, start, stop):
        self.start = float(start)
        self.stop = float(stop)