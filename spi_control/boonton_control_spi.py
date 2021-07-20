from fpga_spi import *
import socket

#Sensor Register designations
SENSOR_REG_JUMP = 0x8
SENSOR_BASE = 0x0
SENSOR_COUNT =  4
SENSOR_STATUS =  0x0
TRIG_SELECT =   0x1
TRIG_STATE =  0x2
SENSOR_RESET = 0x3
SENSOR_CONTROL = 0x4
SENSOR_TIME_LO = 0x5
SAMPLE_TYPE = 0x5
SENSOR_TIME_HI = 0x6
PULSE_SELECT = 0x7

#Raspberry Pi Control Registers. Register map is taken from 
#FPGA code
PI_BASE = 0x40
ERROR_REG = 0
TRIGGER_ARM_REG = 2
LO_IP_REG = 3
HI_IP_REG = 4
'''
API wrapper for writing and reading registers with FPGA
fpga_spi module is the base for this class and controls the lower level 
SPI processes. 
'''
class boonton_control_spi(fpga_spi):
    def __init__(self):
        super().__init__()

    def get_sensor_status(self, sensor):
        err = check_sensor_number(sensor)
        if err:
            return err
        address = (int(sensor) - 1 ) * SENSOR_REG_JUMP + SENSOR_STATUS
        data = self.read_register(address )
        return data

    def set_trigger_select(self, sensor, value):
        err = check_sensor_number(sensor)
        if err:
            return err
        address = (int(sensor) - 1) * SENSOR_REG_JUMP + TRIG_SELECT
        data = self.write_register(address, value)
        return data

    def get_trigger_select(self, sensor):
        err = check_sensor_number(sensor)
        if err:
            return err
        address = (int(sensor) - 1) * SENSOR_REG_JUMP + TRIG_SELECT
        data = self.read_register(address)
        return data

    def get_trigger_state(self, sensor):
        err = check_sensor_number(sensor)
        if err:
            return err
        address = (int(sensor) - 1) * SENSOR_REG_JUMP + TRIG_STATE
        data = self.read_register(address)
        return data

    def sensor_reset(self, sensor):
        err = check_sensor_number(sensor)
        if err:
            return err
        address = (int(sensor) - 1) * SENSOR_REG_JUMP + SENSOR_RESET
        data = self.write_register(address, 1)
        return data

    def get_sensor_reset(self, sensor):
        err = check_sensor_number(sensor)
        if err:
            return err
        address = (int(sensor) - 1) * SENSOR_REG_JUMP + SENSOR_RESET
        data = self.read_register(address)
        return data

    def set_sensor_power(self, sensor, setting):
        if not isinstance(setting, bool):
            return TypeError('setting must be boolean')
    
        err = check_sensor_number(sensor)
        if err:
            return err

        address = (int(sensor) - 1) * SENSOR_REG_JUMP + SENSOR_CONTROL
        self.write_register(address, setting)
            

    def get_sensor_power(self, sensor):
        err = check_sensor_number(sensor)
        if err:
            return err

        address = (int(sensor) - 1) * SENSOR_REG_JUMP + SENSOR_CONTROL
        data = self.read_register(address)
        return data

    def get_sample_type(self, sensor):
        err = check_sensor_number(sensor)
        if err:
            return err

        address = (int(sensor) - 1) * SENSOR_REG_JUMP + SAMPLE_TYPE
        data = self.read_register(address)
        return data

    def get_timestamp(self, sensor):
        err = check_sensor_number(sensor)
        if err:
            return err

        lo_address = (int(sensor) - 1) * SENSOR_REG_JUMP + SENSOR_TIME_LO
        hi_address = (int(sensor) - 1) * SENSOR_REG_JUMP + SENSOR_TIME_HI
        
        data_lo = self.read_register(lo_address)
        data_hi = self.read_register(hi_address)

        usecs = data_lo + ((data_hi & 0xf) << 16)
        seconds = (data_hi >> 4) & 0x3f
        minutes = (data_hi >> 10) & 0x3f

        return f"{minutes}:{seconds}.{usecs}"

    def set_trigger_delay(self, sensor, pulses):
        err = check_sensor_number(sensor)
        if err:
            return err
        address = (int(sensor) - 1) * SENSOR_REG_JUMP + PULSE_SELECT
        self.write_register(address, pulses)

    def get_trigger_delay(self, sensor):
        err = check_sensor_number(sensor)
        if err:
            return err

        address = (int(sensor) - 1) * SENSOR_REG_JUMP + PULSE_SELECT
        data = self.read_register(address)
        return data

    def set_error(self, value):
        address = PI_BASE + ERROR_REG
        data = self.write_register(address, value)

    def get_error(self):
        address = PI_BASE + ERROR_REG
        data = self.read_register(address)

    def set_trigger_arm(self, value):
        address = PI_BASE + TRIGGER_ARM_REG
        data = self.read_register(address, value)
        
    def get_trigger_arm(self):
        address = PI_BASE + TRIGGER_ARM_REG
        data = self.read_register(address)

    def get_ip_address(self):
        lo_address = PI_BASE + LO_IP_REG
        hi_address = PI_BASE + HI_IP_REG

        data_lo = self.read_register(lo_address)
        data_hi = self.read_register(hi_address)
        byte0 = data_lo & 0xff
        byte1 = (data_lo >> 8) & 0xff
        byte2 = data_hi & 0xff
        byte3 = (data_hi >> 8) & 0xff 

        return f"{byte3}.{byte2}.{byte1}.{byte0}"

    def set_ip_address(self, ip_addr):
        parts = ip_addr.split('.')
        low_byte = int(parts[3])
        ip_int = ip_to_int(ip_addr)
        lo_word = ip_int & 0xffff
        hi_word = (ip_int >> 16) & 0xffff

        print(lo_word)
        print(hi_word)
        print(f"Low Byte -> {low_byte}")
        print(f"Low Byte -> {lo_word}")
        print(f"Low Byte -> {hi_word}")

        lo_address = PI_BASE + LO_IP_REG
        hi_address = PI_BASE + HI_IP_REG
        print(self.write_register(lo_address, lo_word))
        print(self.write_register(hi_address, hi_word))
        print(f"Register ip_low = {self.read_register(lo_address)}")
        print(f"Register ip_high = {self.read_register(hi_address)}")

        self.set_error(0)
        print(f"Register 64 = {self.get_error()}")

# def sensor_within_range(sensor):
#     try:
#         sensor = int(sensor)
#         if sensor < 1 or sensor > SENSOR_COUNT:
#             return False
#     except:
#         return False
    
#     return True

def check_sensor_number(sensor):
    try:
        sensor = int(sensor)
    except:
        return TypeError('Type should be an integer')
    if sensor < 1 or sensor > SENSOR_COUNT:
        return ValueError('Sensor number must be with range for the pi.')
    return None

def ip_to_int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int_to_ip(int_value):
    return socket.inet_ntoa(struct.pack("!I", int_value))


