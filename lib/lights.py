"""
lights.py

Code based upon: https://github.com/artem-smotrakov/esp32-weather-google-sheets
class Lights controls LEDs that report the following:
WiFi connection, error, high temperature level, discomfort exceeded

2021-0817 PP added discomfort, removed test
"""
import time
from machine import Pin
import lolin_d1mini as board

class Lights(object):

    # initializes a new instance
    def __init__(self, leds_config):
        # define LEDS
        led_pins = [leds_config.get(i)[0] for i in range(1, len(leds_config)+1)]
        self._leds = [Pin(pin, Pin.OUT) for pin in led_pins]

        # assign meaning to specific LEDs:
        for i in range(1, len(leds_config)+1):
            if 'reserve' in leds_config.get(i):
                #DEBUG: print(led_pins[i-1], self._leds[i-1])
                #OK: self._leds[i-1].value(0) if led_pins[i-1] == board.D0 else self._leds[i-1].value(0)
                self._leds[i-1].off()
            if 'wifi' in leds_config.get(i):
                self.wifi_led = self._leds[i-1]
            if 'error' in leds_config.get(i):
                self.error_led = self._leds[i-1]
            if 'discomfort' in leds_config.get(i):
                self.discomfort_led = self._leds[i-1]
            if 'high_threshold' in leds_config.get(i):
                self.high_threshold_led = self._leds[i-1]
            if 'low_threshold' in leds_config.get(i):
                self.low_threshold_led  = self._leds[i-1]


    def set_wifi_led(self, idx):
        self.wifi_led = self._leds[idx]

    def set_error_led(self, idx):
        self.error_led = self._leds[idx]

    def set_discomfort_led(self, idx):
        self.discomfort_led = self._leds[idx]

    def set_high_threshold_led(self, idx):
        self.high_threshold_led = self._leds[idx]

    def set_low_threshold_led(self, idx):
        self.low_threshold_led = self._leds[idx]

    # turn on the LED for WiFi
    def wifi_on(self):
        self.wifi_led.on()

    # turn off the LED for WiFi
    def wifi_off(self):
        self.wifi_led.off()

    # turn on the LED that reports an error
    def error_on(self):
        self.error_led.on()

    # turn off the LED that reports an error
    def error_off(self):
        self.error_led.off()

    # turn on the LED for discomfort
    def discomfort_on(self):
        self.discomfort_led.on()

    # turn off the LED for discomfort
    def discomfort_off(self):
        self.discomfort_led.off()

    # turn on the LED that reports high threshold level
    def high_threshold_on(self):
        self.high_threshold_led.on()

    # turn off the LED that reports high threshold level
    def high_threshold_off(self):
        self.high_threshold_led.off()

    # turn on the LED that reports low threshold level
    def low_threshold_on(self):
        self.low_threshold_led.on()

    # turn off the LED that reports low threshold level
    def low_threshold_off(self):
        self.low_threshold_led.off()

    # turn off all LEDs
    def off(self):
        self.wifi_off()
        self.error_off()
        self.discomfort_led.off()
        self.high_threshold_off()
        self.low_threshold_off()

    """ 2021-0812 PP added test
    def test(self, dt=1):
        self.off()
        time.sleep(dt)

        print("Wifi connected...")
        self.wifi_on()
        time.sleep(dt)
        
        print("Error condition...")
        self.error_on()
        time.sleep(dt)
        
        print("Temperature > high_threshold...")
        self.high_threshold_on()
        time.sleep(dt)
        
        print("Temperature < low_threshold...")
        self.low_threshold_on()
        time.sleep(dt*5)

        print("Wifi disconnected...")
        self.wifi_off()
        time.sleep(dt)
        
        print("No error condition...")
        self.error_off()
        time.sleep(dt)
        
        print("Temperature < high_threshold...")
        self.high_threshold_off()
        time.sleep(dt)
        
        print("Temperature > low_threshold...")
        self.low_threshold_off()
    """
