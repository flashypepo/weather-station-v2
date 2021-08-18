"""
AHT10Sensor measures temperature and humidity with AHT10 sensor

2021--0816 PP add lights.error_on/off in isDetected()
2021-0812 PP new, driver based upon source


"""
from ahtx0 import AHT10

class AHT10Sensor:

    # initializes a new instance
    def __init__(self, i2c, lights, discomfort_threshold, temperature_thresholds):
        self.aht10 = AHT10(i2c)
        # check if AHT10 sensor is connected
        #TEST: self._isDetected(i2c)
        self.lights = lights
        self.low_threshold = temperature_thresholds[0]
        self.high_threshold = temperature_thresholds[1]
        self.discomfort_threshold = discomfort_threshold

    def calc_discomfort(self, c, h):
        """
            calculate discomfort
            source:
            limits: unknown
        """
        return (0.81 * c) + ((0.01 * h) * ((0.99 * c) - 14.3)) + 46.3


    # measure temperature and humidity
    def measure(self, verbose=False):
        c = self.aht10.temperature
        h = self.aht10.relative_humidity
        f = (c * 1.8) + 32 #PP - WHY int()?: int((c * 1.8) + 32)
        d = self.calc_discomfort(c, h)
        if verbose is True:
            print('Measurements:')
            print('\tcentigrade: {:.2f} C'.format(c))
            print('\tfarenheit : {:.2f} F'.format(f))
            print('\thumidity  : {:.2f} %'.format(h))
            print('\tdiscomfort: {:.2f}'.format(d))
            
            print('Thresholds:')
            print('\tdiscomfort       : {:.2f}'.format(self.discomfort_threshold))
            print('\thigh temperature : {:.2f} C'.format(self.high_threshold))
            print('\tlow temperature  : {:.2f} C'.format(self.low_threshold))
        # set the light indicators
        self.lights.high_threshold_on() if c >= self.high_threshold else self.lights.high_threshold_off()
        self.lights.low_threshold_on() if c <= self.low_threshold else self.lights.low_threshold_off()
        self.lights.discomfort_on() if d >= self.discomfort_threshold else self.lights.discomfort_off()
        # returns measured values
        return [c, h, f]

    def check(self):
        """
            ceck if things needs to be done
            2021-0817 check AHT10 is still connected
        """
        self._isDetected(self.aht10._i2c)

        
    # check if AHT10 sensor is(still)connected
    def _isDetected(self, i2c):
        if (self.aht10.AHTX0_I2CADDR_DEFAULT not in i2c.scan()):
            self.lights.error_on()
            raise Exception("AHT10 sensor not detected or changed I2C address")
        else:
            self.lights.error_off()
            #DEBUG: print("AHT10 sensor detected")
