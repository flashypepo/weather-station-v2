"""
main.py
- measures air quality using SGP30 (d1 minishield) sensor,
- using Lights for:
    - Wifi connection,
    - error condition
    - thresholds exceeded (high and low)
- LED assignment - see class Lights

2021-0816 PP new, code based upon ATH10 environment sensor
             Inspired by https://github.com/artem-smotrakov/esp32-weather-google-sheets
"""
import time
from machine import Pin
from machine import I2C
import sys
import uerrno

import lolin_d1mini as board
from monitor import Monitor
#LATERON: from google.auth import ServiceAccount
#LATERON: from google.sheet import Spreadsheet
import util

# load configuration for device and sensors
# see boot.py for lights
from config import config_device
from config import config_sensors

VERBOSE = True  # prints details or debuggung values

# handling of measured data
# FUTURE TODO: put data in a Google sheet
# TODO: tore data in file
# 2021-0812 PP print data on console
class MonitorHandler:
    # initializes a new handler
    def __init__(self):
        pass

    # process data
    # PP FUTURE TODO:
    # 1. take into account summertime
    # 2. store in file
    # 3. send data to the sheet
    def handle(self, data):
        tm = time.localtime()  # wintertime
        #now = "{0}-{1:02d}-{2},{3:02d}:{4:02d}:{5:02d}".format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])
        #PP: FUTURE TODO for sheet:
        # now = "=TIMESTAMP_TO_DATE(INDIRECT(\"A\" & ROW()))"
        data.append(tm)
        print('MonitorHandler - send the following to a storage: {}'.format(data))
        # self.sheet.append_values(data)

def check_devices(i2c):
    devices = i2c.scan()
    if len(devices) > 0:
        for device in devices:
            print("I2C devices: {}".format(hex(device)))
    else:
        print("no i2c-devies")


try:
    print("\neCO2 monitor...")
    
    # I2C for the Wemos D1 Mini with ESP8266
    i2c = I2C(scl=Pin(board.I2C_SCL), sda=Pin(board.I2C_SDA))
    # define a monitor
    monitor  = Monitor(i2c=i2c,
                       interval=config_device['measurement_interval'],
                       handler=MonitorHandler())

    check_devices(i2c)

    # add sensors from configuration, skip if not specified
    # AHT10 - temperature and humidity sensor
    if config_sensors.get('aht10_sensor') is not None:
        from aht10sensor import AHT10Sensor
        monitor.add(AHT10Sensor(i2c=i2c,
                                lights=lights,
                                discomfort_threshold=config_sensors['discomfort'],
                                temperature_thresholds=config_sensors['temperature_interval'],
                                ))
        print('...registered a AHT10 sensor')

    # SGP30 - air quality sensor
    if config_sensors.get('sgp30_sensor') is not None:
        from sgp30sensor import SGP30Sensor
        sgp30sensor = SGP30Sensor(i2c=i2c,
                                  lights=lights,
                                  thresholds=config_sensors['co2_threshold'])
        monitor.add(sgp30sensor)
        print('...registered a SGP30 sensor')

    """ FUTURE PLAN
    if config_sensors.get('dht22_sensor') is not None:
        from dht22sensor import DHT22Sensor
        monitor.add(DHT22Sensor(config_sensors['dht22_sensor']))
        print('...registered a DHT22 sensor')

    if config_sensors.get('mhz19b_sensor') is not None:
        from mhz19bsensor import MHZ19BSensor
        monitor.add(MHZ19BSensor(pins=config_sensors['mhz19b_sensor'],
                                 lights=lights,
                                 threshold=config_sensors['co2_threshold']))
        print('...registered a MH-Z19B sensor')

    if config_sensors.get('bme280_sensor') is not None:
        from bme280sensor import BME280Sensor
        monitor.add(BME280Sensor(i2c=i2c,
                                 lights=lights,
                                 thresholds=config_sensors['temperature_interval']))
        print('...registered a BME280 sensor')
    """

    # start the main loop
    # in the loop, the board is going to check temperature and humidity
    lights.error_off()
    error = False
    while True:
            # reconnect if a error occurred or the connection is lost
        if error or not wifi.is_connected():
            wifi.reconnect()

        error = False
        lights.error_off()
        
        monitor.measure()
        monitor.check()

        # a little delay
        time.sleep(monitor.interval)
        #DEBUG: print("Memory: {} kB".format(gc.mem_free() // 1024))

except Exception as e:
    error = True
    lights.error_on()
    print('Something wrong happened! ...')
    sys.print_exception(e)
    
    if isinstance(e, OSError) and e.args[0] in uerrno.errorcode:
        print('error code: %s' % uerrno.errorcode[e.args[0]])

    if config_device['error_handling'] == 'reboot':
        print('rebooting ...')
        util.reboot()

    if config_device['error_handling'] == 'stop':
        print('stop ...')
        raise
    else:
        print('continue ...')

except OSError as ex:
    lights.error_on()
    print("main - OSError: {}".format(ex))

except KeyboardInterrupt:
    print("\nUser interrupt, done.")

finally:
    gc.collect()
    print("Memory: {} kB".format(gc.mem_free() // 1024))
