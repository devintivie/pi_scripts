import os
import sys

from ctypes import *
from boonton_helpers import *

CHANNEL_STRING = "CH1"
class boonton_55318:
    def __init__(self, lib, serial_num):
        self._lib = lib
        self.serial = serial_num
        self._handle = None
        self.trig_settings = dict()
        self.traces = dict()
        self.gates= dict()
        self.trace_sum = dict()
        self.trace_fresh = dict()

    

    def initialize(self):
        if not self._handle:
            c_handle = c_int()
            ans = self._lib.Btn55xxx_init(f"USB::0x1BFE::0x5500::{self.serial}::BTN", byref(c_handle))
            if ans:
                print(f'ERROR: {ans}')
            else:
                self._handle = c_handle

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
    def set_trig_settings(self):
        self.update_trig_settings()

    def update_trig_settings(self):
        self.update_timebase()
        self.update_timespan()
        self.update_trig_level()
        self.update_trig_mode()
        self.update_trig_slope()
        self.update_trig_position()
        self.update_trig_delay()
        self.update_trig_holdoff()
        self.update_trig_source()
        self.update_average()
        self.update_bandwidth()
        self.update_units()
        self.update_frequency()

    def update_timebase(self):
        c_timebase = c_float()
        ans = self._lib.Btn55xxx_GetTimebase(self._handle, byref(c_timebase))
        self.trig_settings['timebase'] = c_timebase.value
    
    def update_timespan(self):
        c_timespan = c_float()
        self._lib.Btn55xxx_GetTimespan(self._handle, byref(c_timespan))
        self.trig_settings['timespan'] = c_timespan.value

    def update_trig_level(self):
        c_trig_level = c_float()
        self._lib.Btn55xxx_GetTrigLevel(self._handle, byref(c_trig_level))
        self.trig_settings['trig_level'] = c_trig_level.value

    def update_trig_mode(self):
        c_trig_mode = c_int()
        self._lib.Btn55xxx_GetTrigMode(self._handle, byref(c_trig_mode))
        self.trig_settings['trig_mode'] = c_trig_mode.value

    def update_trig_slope(self):
        c_trig_slope = c_int()
        self._lib.Btn55xxx_GetTrigMSlope(self._handle, byref(c_trig_slope))
        self.trig_settings['trig_slope'] = c_trig_slope.value

    def update_trig_position(self):
        c_trig_position = c_float()
        self._lib.Btn55xxx_GetTrigVernier(self._handle, byref(c_trig_position))
        self.trig_settings['trig_position'] = c_trig_position.value

    def update_trig_delay(self):
        c_trig_delay = c_float()
        self._lib.Btn55xxx_GetTrigDelay(self._handle, byref(c_trig_delay))
        self.trig_settings['trig_delay'] = c_trig_delay.value

    def update_trig_holdoff(self):
        c_trig_holdoff = c_float()
        self._lib.Btn55xxx_GetTrigHoldoff(self._handle, byref(c_trig_holdoff))
        self.trig_settings['trig_holdoff'] = c_trig_holdoff.value

    def update_trig_source(self):
        c_trig_source = c_int()
        self._lib.Btn55xxx_GetTrigSource(self._handle, byref(c_trig_source))
        self.trig_settings['trig_source'] = c_trig_source.value

    def update_average(self):
        c_average = c_int()
        self._lib.Btn55xxx_GetAverage(self._handle, byref(c_average))
        self.trig_settings['average'] = c_average.value

    def update_bandwidth(self):
        c_bandwidth = c_int()
        self._lib.Btn55xxx_GetBandwidth(self._handle, byref(c_bandwidth))
        self.trig_settings['video_bandwidth'] = c_bandwidth.value

    def update_units(self):
        c_unit = c_int()
        self._lib.Btn55xxx_GetUnits(self._handle, byref(c_unit))
        self.trig_settings['units'] = c_unit.value

    def update_frequency(self):
        c_frequency = c_float()
        self._lib.Btn55xxx_GetFrequency(self._handle, byref(c_frequency))
        self.trig_settings['frequency'] = c_frequency.value

    

    

    



        