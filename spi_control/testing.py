from ctypes import ArgumentError


SENSOR_COUNT =  4

class testing:
    # def get_trigger_select(self, sensor):
    #     if sensor_within_range(sensor):
    #         print('continue')
    #     else:
    #         print('error')
    #         return 'Sensor number must be with range for the pi.'

    def get_trigger_select(self, sensor):
        err = check_sensor_number(sensor)
        if err:
            return err
        else:
            return 2


def sensor_within_range(sensor):
    try:
        sensor = int(sensor)
    except:
        return False
    if sensor < 1 or sensor > SENSOR_COUNT:
        return False
    return True

def check_sensor_number(sensor):
    try:
        sensor = int(sensor)
    except:
        return ArgumentError('Argument should be an integer')
    if sensor < 1 or sensor > SENSOR_COUNT:
        return ValueError('Sensor number must be with range for the pi.')
    return None




test = testing()

success = test.get_trigger_select(sensor=1)
print(success)
success = test.get_trigger_select(sensor=4)
print(success)
success = test.get_trigger_select(sensor=5)
print(success)
success = test.get_trigger_select(sensor='5')
print(success)
success = test.get_trigger_select(sensor='sensor5')
print(success)
