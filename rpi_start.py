import socket
import fcntl
from fpga_spi import *

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15], 'utf-8')))[20:24])
    s = None
    return ip_address

def ip_to_int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int_to_ip(intValue):
    return socket.inet_ntoa(struct.pack("!I", intValue))

ip_addr = get_ip_address('eth0')
print(f"IP Address -> {ip_addr} ({type(ip_addr)})")

parts = ip_addr.split('.')
low_byte = int(parts[3])
lo_word = ip_to_int(ip_addr) & 0xffff
hi_word = (ip_to_int(ip_addr) >> 16) & 0xffff

print(lo_word)
print(hi_word)
print(f"Low Byte -> {low_byte}")

spi = fpga_spi()

spi.write_register(67, lo_word)
spi.write_register(68, hi_word)
print(f"Register 67 = {spi.read_register(67)}")
print(f"Register 68 = {spi.read_register(68)}")

spi.write_register(64, 0)
print(f"Register 64 = {spi.read_register(64)}")