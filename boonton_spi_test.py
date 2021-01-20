from boonton_control_spi import *

fpga = boonton_control_spi()

# print(fpga.get_ip_address())

print(fpga.write_register(0x105, 50))
for i in range(4):
    print(fpga.get_trigger_select(i+1))

for i in range(4):
    print(fpga.set_sensor_power(i+1, False))

for i in range(4):
    print(fpga.get_sensor_power(i+1))

