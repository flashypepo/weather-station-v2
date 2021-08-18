"""
SGP30Sensor measures eCO2 and TVOC with Lolin SGP30-minishield

TVOC bereik: 0-60000ppb
eCO2 bereik: 400-60000ppm

2021-0816 PP new
"""
import time
import adafruit_sgp30

VERBOSE = False  # global debugging or not

class SGP30Sensor:

    # initializes a new instance
    def __init__(self, i2c, lights=None, thresholds=[400, 1000]):
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        if VERBOSE is True:
            print("SGP30 serial #", [hex(i) for i in self.sgp30.serial])
        # Initialize SGP-30 internal drift compensation algorithm.
        self.sgp30.iaq_init()
        self.lights = lights
        self.low_threshold = thresholds[0]
        self.high_threshold = thresholds[1]
        self._has_baseline = False
        self._baseline_time = time.time() # time of 'last saved' baseline values
        
        # Wait 15 seconds for the SGP30 to properly initialize
        print("Waiting 15 seconds for SGP30 initialization.")
        time.sleep(15)

    def read_baseline_values(self):
        """
        returns: has_baseline
            has_baseline=True : valid values for co2_baseline, tvoc_baseline
            has_baseline=False: cno values for o2_baseline, tvoc_baseline
        """
        print('Reading SGP30 baselines from files!')
        has_baseline = False
        
        try:
            f_co2 = open('co2eq_baseline.txt', 'r')
            f_tvoc = open('tvoc_baseline.txt', 'r')

            co2_baseline = int(f_co2.read())
            tvoc_baseline = int(f_tvoc.read())
            #Use them to calibrate the sensor
            self.sgp30.set_iaq_baseline(co2_baseline, tvoc_baseline)

            f_co2.close()
            f_tvoc.close()

            has_baseline = True
        except:
            print('Impossible to read SGP30 baselines!')

        self._has_baseline = has_baseline
        return has_baseline

    def write_baseline_values(self):
        print('Writing SGP30 baselines to files!')
        try:
            f_co2 = open('co2eq_baseline.txt', 'w')
            f_tvoc = open('tvoc_baseline.txt', 'w')

            bl_co2, bl_tvoc = self.sgp30.get_iaq_baseline()
            f_co2.write(str(bl_co2))
            f_tvoc.write(str(bl_tvoc))

            f_co2.close()
            f_tvoc.close()

            has_baseline = True
            #Store the time at which last baseline has been saved
            self._baseline_time = time.time()
            self._has_baseline = has_baseline

        except:
            print('Impossible to write SGP30 baselines!')

        return has_baseline
        
    # measure sensor values
    def measure(self, verbose=False):
        # read sensorvalues
        co2eq, tvoc = self.sgp30.iaq_measure()

        if verbose is True:
            #print('co2eq = ' + str(co2eq) + ' ppm \t tvoc = ' + str(tvoc) + ' ppb')
            print('eCO2: {:} ppm \tTVOC : {:} ppb'.format(co2eq, tvoc))
            print('thresholds: [{:}, {:}]'.format(self.low_threshold, self.low_threshold))
        
        # set light indicators
        #self.lights.high_threshold_on() if c >= self.high_threshold else self.lights.high_threshold_off()
        #self.lights.low_threshold_on() if c <= self.low_threshold else self.lights.low_threshold_off()

        return [co2eq, tvoc]


    def check(self):
        """
            Baselines SGP30 sensor should be saved after 12 hour the first timen
            then every hour, according to the doc.
        """
        delta_time = time.time() - self._baseline_time
        if (self._has_baseline and (delta_time >= 3600)) \
            or ((not self._has_baseline) and (delta_time >= 43200)):
            #print('Saving SGP30-baseline!')
            self._baseline_time = time.time()
            self._has_baseline = self.write_baseline_values()
