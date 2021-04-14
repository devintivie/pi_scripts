import os
import sys

from ctypes import *
from boonton_helpers import *
import math

CHANNEL_STRING = "CH1"
TRACE_LENGTH = 501
DEFAULT_POWER = -30.0
class boonton_55318:
    def __init__(self, lib, serial_num, config, publisher):
        self._lib = lib
        self.serial = serial_num
        self._handle = None
        self.config = config
        self.trig_settings = dict()
        self.trace = dict()
        self.gates= list()
        self.trace_sum = dict()
        self.trace_fresh = dict()
        self.publisher = publisher

    def initialize(self):
        if self._handle:
            c_handle = c_int()
            try:
                ans = self._lib.Btn55xxx_init(f"USB::0x1BFE::0x5500::{self.serial}::BTN", byref(c_handle))
                if ans:
                    print(f'ERROR: {ans}')
                else:
                    self._handle = c_handle
            except Exception as ex :
                print(f'init exception {ex}')

    def close(self):
        if self._handle:
            ans = self._lib.Btn55xxx_close(self._handle)
            if ans:
                print(f"ERROR: close{self.serial} -> {ans}")
            else:
                self._handle = None

    def reset(self):
        if self._handle:
            ans = self._lib.Btn55xxx_reset(self._handle)
            if ans:
                print(f"ERROR: reset {self.serial} -> {ans}")

    def get_current_temp(self):
        if self._handle:
            c_temp = c_double()
            ans = self._lib.Btn55xxx_GetCurrentTemp(self._handle, CHANNEL_STRING, byref(c_temp))
            if ans:
                print(f'ERROR: get_temp {self.serial} -> {ans}')
                return 0.0
        return c_temp.value


    '''TRIGGERS'''
    # def set_trig_settings(self):
    #     self.update_trig_settings()

    def update_trig_settings(self):
        self.get_timebase()
        self.get_timespan()
        self.get_trig_level()
        self.get_trig_mode()
        self.get_trig_slope()
        self.get_trig_position()
        self.get_trig_delay()
        self.get_trig_holdoff()
        self.get_trig_source()
        self.get_average()
        self.get_bandwidth()
        self.get_units()
        self.get_frequency()
    
    def get_trig_settings(self):
        self.get_trig_settings()
        return self.trig_settings

    def set_timebase(self, timebase):
        "Set trace time per division (5E-9 to 50E-3, 10 divisions per trace)"
        valid_times = (5e-9, 10e-9, 20e-9, 50e-9, 100e-9, 200e-9, 500e-9,
                1e-6, 2e-6, 5e-6, 10e-6, 20e-6, 50e-6, 100e-6, 200e-6,
                500e-6, 1e-3, 2e-3, 5e-3, 10e-3, 20e-3, 50e-3)
        if timebase in valid_times:
            c_timebase = c_float(timebase)
            usb_error = self._lib.Btn55xxx_SetTimebase(self._handle, c_timebase)
            return usb_error
        else:
            print('ERROR : Sensor adjusted invalid timebase')
            return None

    def get_timebase(self):
        c_timebase = c_float()
        usb_error = self._lib.Btn55xxx_GetTimebase(self._handle, byref(c_timebase))
        self.trig_settings['timebase'] = c_timebase.value
        return usb_error
    
    def set_timespan(self, timespan):
        "Set trace time per division (5E-9 to 50E-3, 10 divisions per trace)"
        valid_times = (50e-9, 100e-9, 200e-9, 500e-9, 1e-6, 2e-6, 5e-6, 10e-6, 
                20e-6, 50e-6, 100e-6, 200e-6, 500e-6, 1e-3, 2e-3, 5e-3, 10e-3, 
                20e-3, 50e-3, 100e-3, 200e-3, 500e-3)
        if timespan in valid_times:
            c_timespan = c_float(timespan)
            usb_error = self._lib.Btn55xxx_SetTimespan(self._handle, c_timespan)
            return usb_error
        else:
            print('ERROR : Sensor adjusted invalid timespan')
            return None

    def get_timespan(self):
        c_timespan = c_float()
        usb_error = self._lib.Btn55xxx_GetTimespan(self._handle, byref(c_timespan))
        self.trig_settings['timespan'] = c_timespan.value
        return usb_error

    def set_trig_level(self, level):
        "Set trigger level in dBm"
        c_level = c_float(level)
        usb_error = self._lib.Btn55xxx_SetTrigLevel(self._handle, c_level)
        return usb_error

    def get_trig_level(self):
        c_trig_level = c_float()
        usb_error = self._lib.Btn55xxx_GetTrigLevel(self._handle, byref(c_trig_level))
        self.trig_settings['trig_level'] = c_trig_level.value
        return usb_error

    def set_trig_mode(self, mode, scpi = False):
        if scpi:
            if mode == boonton_trigger_mode.normal:
                usb_error = self.send_scpi_command("TRIG:MODE NORMAL")
            else:
                raise ArgumentError('Method not typically used, double check usage')
        else:
            if isinstance(mode, boonton_trigger_mode):
                c_mode = c_int(mode.value)
                usb_error = self._lib.Btn55xxx_SetTrigMode(self._handle, c_mode)
                return usb_error
            return b'invalid mode error'

    def get_trig_mode(self):
        c_trig_mode = c_int()
        self._lib.Btn55xxx_GetTrigMode(self._handle, byref(c_trig_mode))
        self.trig_settings['trig_mode'] = c_trig_mode.value

    def set_trig_slope(self, slope):
        c_slope = c_int(slope.value)
        usb_error = self._lib.Btn55xxx_SetTrigSlope(self._handle, c_slope)
        return usb_error

    def get_trig_slope(self):
        c_trig_slope = c_int()
        self._lib.Btn55xxx_GetTrigMSlope(self._handle, byref(c_trig_slope))
        self.trig_settings['trig_slope'] = c_trig_slope.value

    def set_trig_position(self, position):
        c_trig_position = c_float(position.value)
        usb_error = self._lib.Btn55xxx_SetTrigVernier(self._handle, c_trig_position)
        return usb_error

    def get_trig_position(self):
        c_trig_position = c_float()
        self._lib.Btn55xxx_GetTrigVernier(self._handle, byref(c_trig_position))
        self.trig_settings['trig_position'] = c_trig_position.value

    def set_trig_delay(self, delay):
        c_trig_delay = c_int(delay.value)
        usb_error = self._lib.Btn55xxx_SetTrigDelay(self._handle, c_trig_delay)
        return usb_error

    def get_trig_delay(self):
        c_trig_delay = c_float()
        self._lib.Btn55xxx_GetTrigDelay(self._handle, byref(c_trig_delay))
        self.trig_settings['trig_delay'] = c_trig_delay.value

    def set_trig_holdoff(self, holdoff):
        c_trig_holdoff = c_float(holdoff.value)
        usb_error = self._lib.Btn55xxx_SetTrigHoldoff(self._handle, c_trig_holdoff)
        return usb_error

    def get_trig_holdoff(self):
        c_trig_holdoff = c_float()
        self._lib.Btn55xxx_GetTrigHoldoff(self._handle, byref(c_trig_holdoff))
        self.trig_settings['trig_holdoff'] = c_trig_holdoff.value

    def set_trig_source(self, source):
        c_trig_source = c_int(source.value)
        usb_error = self._lib.Btn55xxx_SetTrigSource(self._handle, c_trig_source)
        return usb_error

    def get_trig_source(self):
        c_trig_source = c_int()
        self._lib.Btn55xxx_GetTrigSource(self._handle, byref(c_trig_source))
        self.trig_settings['trig_source'] = c_trig_source.value

    def set_average(self, average):
        c_average = c_int(average.value)
        usb_error = self._lib.Btn55xxx_SetAverage(self._handle, c_average)
        return usb_error

    def get_average(self):
        c_average = c_int()
        self._lib.Btn55xxx_GetAverage(self._handle, byref(c_average))
        self.trig_settings['average'] = c_average.value

    def set_bandwidth(self, bandwidth):
        c_bandwidth = c_float(bandwidth.value)
        usb_error = self._lib.Btn55xxx_SetBandwidth(self._handle, c_bandwidth)
        return usb_error

    def get_bandwidth(self):
        c_bandwidth = c_int()
        self._lib.Btn55xxx_GetBandwidth(self._handle, byref(c_bandwidth))
        self.trig_settings['video_bandwidth'] = c_bandwidth.value

    def set_units(self, units):
        if isinstance(units, boonton_units):
            c_units = c_int(units.value)
            usb_error = self._lib.Btn55xxx_SetUnits(self._handle, c_units)
            return usb_error
        return b'unit error'

    def get_units(self):
        c_unit = c_int()
        self._lib.Btn55xxx_GetUnits(self._handle, byref(c_unit))
        self.trig_settings['units'] = c_unit.value

    def set_frequency(self, frequency):
        c_frequency = c_float(frequency.value)
        usb_error = self._lib.Btn55xxx_SetFrequency(self._handle, c_frequency)
        return usb_error

    def get_frequency(self):
        c_frequency = c_float()
        self._lib.Btn55xxx_GetFrequency(self._handle, byref(c_frequency))
        self.trig_settings['frequency'] = c_frequency.value

    def set_continuous_measurement(self, onoff):
        if onoff:
            setting = 1
        else:
            setting = 0
                   
        usb_error = self._lib.SetInitiateContinuous(self._handle, c_int(setting))

    def send_scpi_command(self, string):
        byte_string = bytes(string, encoding = 'utf-8')
        scpi = create_string_buffer(byte_string)
        usb_error = self._lib.Btn55xxx_SendSCPICommand(self._handle, scpi)
        return usb_error

    def set_arm_trigger(self):
        "Arm trigger and start continuous measurements"
        usb_error = self.send_scpi_command("TRIG:CDF:CAPT OFF")

        self.set_trig_mode(boonton_trigger_mode.normal, scpi=True)

        self.set_continuous_measurement(True)

    def set_trigger_abort(self):
        usb_error = self._lib.Btn55xxx_Abort(self._handle)
        if usb_error:
            print(f'ERROR: {usb_error} : trigger abort {self.serial}')

    def get_trigger_status(self):
        c_status = c_int()
        usb_error = self._lib.Btn55xxx_GetTrigStatus(self._handle, byref(c_status))
        if usb_error :
            print(f'ERROR : {usb_error} : get status {self.serial}')

    '''TRACE FUNCTIONS'''
    def trace_read(self):
        '''Read a 501-point trace from sensor. If trigger is stopped, 
        sensor single-triggers. If no trigger is present, all NaNs are returns'''
        self.trace.clear()
        self.trace = None
        self.trace_fresh = True # for gate read

        actual_size = c_int()
        trace = c_float * TRACE_LENGTH
        trace = trace(*list([DEFAULT_POWER for i in range(TRACE_LENGTH)]))

        usb_error = self._lib.Btn55xxx_FetchWaveform(self._handle, CHANNEL_STRING, 
                                        TRACE_LENGTH, trace, byref(actual_size))

        if usb_error:
            print(f'ERROR: {usb_error} : trace read {self.serial} {actual_size.value}')
        
        #Handle trace data
        #Default data is float or string???
        for val in trace:
            if math.isnan(val) or val < DEFAULT_POWER:
                val = DEFAULT_POWER

        self.trace = trace

    def trace_read_blocking(self):
        '''Read a 501-point trace from sensor. If trigger is stopped, 
        sensor single-triggers. If no trigger is present, all NaNs are returns'''
        self.trace.clear()
        self.trace = None
        self.trace_fresh = False # for gate read

        actual_size = c_int()
        trace = c_float * TRACE_LENGTH
        trace = trace(*list([DEFAULT_POWER for i in range(TRACE_LENGTH)]))

        usb_error = self._lib.Btn55xxx_FetchWaveform(self._handle, CHANNEL_STRING, 
                                        TRACE_LENGTH, trace, byref(actual_size))

        if usb_error:
            print(f'ERROR: {usb_error} : trace read {self.serial} {actual_size.value}')
        
        #Handle trace data
        #Default data is float or string???
        for val in trace:
            if math.isnan(val) or val < DEFAULT_POWER:
                val = DEFAULT_POWER

        #check for stale data
        #TODO
        # this_sum = sum(trace)
        self.trace = trace

    def save_trace(self):
        "Call read_trace and save results"
        self.trace_read()
        
    '''GATE FUNCTIONS'''
    def calc_gates(self):
        pulse_count = self.config['pulse_count']
        delay = self.config['delay']
        interval = self.config['pri']
        pw = self.config['pw']

        gates = list()
        for pulse in range(pulse_count):
            start = delay + pulse * interval
            stop = start + pw

            gates.append(collect_gate(start, stop))

        return gates

    def set_gates(self, gates):
        self.gates = gates

    def set_gates_from_calc(self):
        gates = self.calc_gates()
        self.set_gates(gates)

    def get_gates_from_config_array(self):
        config_gates = self.config[self.serial]['gates']
        gates = list()
        for gate in config_gates:
            new_gate = collect_gate(gate['start'], gate['stop'])
            gates.append(new_gate)

        return gates

    def set_gates_from_array(self):
        gates = self.get_gates_from_config_array()
        self.set_gates(gates)

    def get_gates(self):
        for i in range(len(self.gates)):
            print(f'gate{i+1} = ({self.gates[i].start} --> {self.gates[i].stop}')

    def get_pulse_data(self):
        #returns gate values data, need to call trace_read first for fresh readings
        xmin = self.trig_settings['trig_position']
        xmax = self.trig_settings['timespan'] - xmin

        for gate_index in range(len(self.gates)):
            gate = self.gates[gate_index]
            freq = self.config['pm_freqs'][gate_index]

            gate_start = gate.start
            gate_stop = gate.stop
            if gate_start < xmin:
                gate_start = xmin
            if gate_stop > xmax:
                gate_stop = xmax
            if gate_stop < gate_start:
                gate_stop = gate_start

            x_index1 = int(round( (gate_start - xmin) / (xmax - xmin) * 500 ) )
            x_index2 = int(round( (gate_stop - xmin) / (xmax - xmin) * 500 ) + 1)

            gate_mean = sum(self.trace[x_index1:x_index2]) / (x_index2 - x_index1)

            if not self.trace_fresh:
                gate_mean = -30.0

            return gate_mean

            


    def timer_tick(self):
        #Poll power meters

        poll = self.poll_data(pull_trace)




    
    

    

    



        