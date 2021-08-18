# This file is executed on every boot (including wake-boot from deepsleep)
import micropython
micropython.alloc_emergency_exception_buf(100)

#import esp
#esp.osdebug(None)
#import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()

# Wifi conection
from wifi import Connection
from secrets import secrets

# Lights
from lights import Lights
# ATH10-sensor:
#from config import config_leds_aq as config_leds
# SGP30 sensor:
from config import config_leds_aq as config_leds

# define lights
lights = Lights(config_leds)
lights.off()

# try to connect to WiFi
wifi = Connection(secrets.get('ssid'), secrets.get('password'), lights)
wifi.connect()

gc.collect()

# enable garbage collection
gc.enable()
print('garbage collection threshold: ' + str(gc.threshold()))
print("Memory: {} kB".format(gc.mem_free() // 1024))
