
commands = {
    "heartbeat" : lambda x : response_heartbeat(x),
    # "identity" : response_identity
}

def process_command(data):
    command = data.command
    payload = data.payload

    response = commands[command](payload)

def response_heartbeat(payload):
    # try:
    mac = getMAC('wlan0')
    ip = get_if_ip('wlan0')
    # except :
    #     return "Bloody Error In'it?" 
    if_list = list('eth0', 'wlan0')
    response = status_check(name=name, if_list=if_list)
    response.status = "ok"
    # status = "ok"
    # response_dict = {

    #     "status" : status
    # }
    return response.__dict__

def getMAC(interface='eth0'):
    try:
        name = open(f'/sys/class/net/{interface}/address').read()
    except:
        name = "00:00:00:00:00:00"
    return name[:17]

def get_if_ip(interface='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_address = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(interface[:15], 'utf-8')))[20:24])
    s = None
    return ip_address