import json

class status_check(object):
    def __init__(self, name, if_list):
        self.name = name
        self.interfaces = list()
        for iface in if_list:
            self.interfaces.append(json.dumps(iface.__dict__))

class if_info(object):
    def __init__(self, if_name, mac, ip):
        self.name = if_name
        self.mac = mac
        self.ip = ip