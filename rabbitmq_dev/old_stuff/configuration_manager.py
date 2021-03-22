import json

class configuration_manager(object):
    def __init__(self, data):
        for key, val in data.items():
            setattr(self, key, self.compute_attr_value(val))

    def compute_attr_value(self, value):
        if type(value) is list:
            return [self.compute_attr_value(x) for x in value]
        elif type(value) is dict:
            return configuration_manager(value)
        else:
            return value


class dict_mapper(object):
    def __init__(self, data):
        for key, val in data.items():
            setattr(self, key, self.compute_attr_value(val))

    def compute_attr_value(self, value):
        if type(value) is list:
            return [self.compute_attr_value(x) for x in value]
        elif type(value) is dict:
            return dict_mapper(value)
        else:
            return value
