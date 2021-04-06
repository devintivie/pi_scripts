import socket
try:
    import fcntl
except:
    pass
import struct

def getMAC(interface='eth0'):
    try:
        name = open('/sys/class/net/'+interface+'/address').read()
    except:
        name = "00:00:00:00:00:00"
    return name[:17]

def get_if_ip(interface='eth0'):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(interface[:15], 'utf-8')))[20:24])
    except OSError:
        ip_address = 'if down'
    s = None
    return ip_address

class callable_dict(dict):
    def __getitem__(self, key):
        val = super().__getitem__(key)
        if callable(val):
            return val()
        return val