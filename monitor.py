"""
class Monitor - measures environment data from various sensors

2021-0816 PP changed name to Monitor, add check()
2021-0812 first version

"""
import time

class Monitor(object):
    __VERSION__ = "2021-0816"
    
    def __init__(self, i2c, interval, thresholds=None, handler=None):
        self.last_measurement = None   # PP: FUTURE TODO
        self.interval = interval # in seconds PP: FUTURE TODO: util.string_to_millis(interval)
        self.handler = handler
        self.thresholds = thresholds
        self.sensors = []
        print("Monitor version: {}".format(self.__VERSION__))  # DEBUG


    # add a sensor
    def add(self, sensor):
        self.sensors.append(sensor)
        
    # measure everything and send the measurements to the handler
    def measure(self):
        data = []
        for sensor in self.sensors:
            measurement = sensor.measure(verbose=False)
            data = data + measurement

        if self.handler is not None:
            self.handler.handle(data)

        #FUTURE TODO? time.sleep(self.interval)

    # each sensor is checked if it has something to do
    # 2021-0816 SGP30 sensor - it does!
    def check (self):
        for sensor in self.sensors:
            sensor.check()


if __name__ == "__main__":
    from machine import Pin, I2C
    import lolin_d1mini as board
    from monitor import EnvironmentMonitor
    
    print("Monitor...")
    # I2C for the Wemos D1 Mini with ESP8266
    # ORG: i2c = I2C(scl=Pin(5), sda=Pin(4))
    i2c = I2C(scl=Pin(board.I2C_SCL), sda=Pin(board.I2C_SDA))
    print("I2C devices: {}".format(i2c.scan()))


    # handling of measured data
    # FUTURE TODO: put data in a Google sheet
    # TODO: tore data in file
    # 2021-0812 PP print data on console
    class MonitorHandler:

        # initializes a new handler
        def __init__(self):
            pass

        # send data to the sheet
        def handle(self, data):
            now = "=TIMESTAMP_TO_DATE(INDIRECT(\"A\" & ROW()))"
            data.append(now)
            print('send the following to a storage: {}'.format(data))
            # self.sheet.append_values(data)



    try:
        monitor  = Monitor(i2c=i2c,
                           interval=configuration['measurement_interval'],
                           handler=MonitorHandler())
        print("version: {}".format(monitor.__VERSION__))  # DEBUG

        # add sensors from configuration, skip if not specified
        if configuration['dht22_sensor']:
            monitor.add(DHT22Sensor(configuration['dht22_sensor']))
            print('registered a DHT22 sensor')

        if configuration['aht10_sensor']:
            monitor.add(AHT10Sensor(i2c,
                                    lights,
                                    configuration['temperature_interval']))
            print('registered a AHT10 sensor')

        if configuration['mhz19b_sensor']:
            monitor.add(MHZ19BSensor(configuration['mhz19b_sensor'],
                                     lights,
                                     configuration['co2_threshold']))
            print('registered a MH-Z19B sensor')

        while True:
            monitor.measure()
            #monitor.check()
            time.sleep(monitor.interval)


    except KeyboardInterrupt:
        print("User interrupt, done.")
