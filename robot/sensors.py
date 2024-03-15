import machine, time
from machine import Pin

""" Ultrasonic Sensor """
class HCSR04():
    __version__ = '0.2.0'
    __author__ = 'Roberto Sánchez'
    __license__ = "Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0"
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.
    The timeouts received listening to echo pin are converted to OSError('Out of range')
    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        self.echo_timeout_us = echo_timeout_us
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self) -> None:
        self.trigger.value(0)
        time.sleep_us(5)
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110:
                raise OSError('Out of range')
            raise ex

    def GetDistance(self):
        """ Return distance in mm. """
        pulse_time = self._send_pulse_and_wait()
        mm = pulse_time * 100 // 582
        return mm

""" Color sensor """
class TCS3200(object):
    def __init__(self) -> None:
        pass

""" Line following sensor """
class HCS301(object):
    def __init__(self, d1, d2, d3, d4, d5, d6, d7, d8, IR) -> None:
        pass