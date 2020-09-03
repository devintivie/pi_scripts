import spidev
from time import sleep
import struct

class fpga_spi:
    clk_freq = int(4.0e6)
    
    def __init__(self):
        self._spi = spidev.SpiDev()
        self.open()
        sleep(2)
        self._spi.mode=0

    def __del__(self):
        self.close()

    def open(self, bus=0, slave=0):
        self._spi.open(bus, slave)
        self.set_clk_freq(self.clk_freq)
        #sleep(2)

    def close(self):
        self._spi.close()

    def set_clk_freq(self, freq):
        self._spi.max_speed_hz = freq

    def write_register(self, raw_addr, raw_data, printdata = False):
        address = raw_addr & 0xffff
        data = raw_data & 0xffff

        if printdata:
            print(f"address = {address}")
            print(f"data = {data}")
        register_list = list([x for x in struct.pack('>H', address)])
        data_list = list([x for x in struct.pack('>H', data)])
        register_list[0] = register_list[0] & 0x7f

        for i in range(len(data_list)):
            register_list.append(data_list[i])

        return_data = self._spi.xfer(register_list)

        int_data = return_data[3] + (return_data[2] << 8)
        return int_data


    def read_register(self, raw_addr):
        address = raw_addr & 0xffff
        register_list = list([x for x in struct.pack('>H', address)])
        register_list[0] = register_list[0] & 0x7f
        register_list.append(0)
        register_list.append(0)
        return_data = self._spi.xfer(register_list)
        int_data = return_data[3] + (return_data[2] << 8)
        return int_data


if __name__ == "__main__":
    spi = fpga_spi()
    sleep(1)
    print('hello')
    print(spi.write_register(1000, 10))
    print(spi.write_register(100, 10))
    print(spi.read_register(1000))
    print(spi.read_register(100))
    spi.close()
