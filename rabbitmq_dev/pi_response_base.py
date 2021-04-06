import json

class status_check(object):
    def __init__(self,if_list): # name, 
        # self.name = name
        self.interfaces = list()
        for iface in if_list:
            self.interfaces.append(iface.__dict__)

class command_response(object):
    pass
    

class if_info(object):
    def __init__(self, if_name, mac, ip):
        self.name = if_name
        self.mac = mac
        self.ipaddress = ip