""" Helper file for the Wemos D1 Mini
    https://wiki.wemos.cc/products:d1:d1_mini

2019-0916
    added const() and prefixes according to my style
    downloaded from https://github.com/mattytrentini/micropython_workshop/
"""
from micropython import const

# Pins
D0 = GPIO16 = const(16)
D1 = GPIO5 = I2C_SCL = const(5)
D2 = GPIO4 = I2C_SDA = const(4)
D3 = GPIO0 = const(0)  # 10k pull-up
D4 = GPIO2 = BUILTIN_LED = const(2)  # 10k pull-up
D5 = GPIO14 = SPI_SCK = const(14)
D6 = GPIO12 = SPI_MISO = const(12)
D7 = GPIO13 = SPI_MOSI = const(13)
D8 = GPIO15 = SPI_SS = SPI_CS = const(15)  # 10k pull-down

# other GPIO pins
GPIO3 = const(3)
GPIO6 = const(6)
GPIO7 = const(7)
GPIO8 = const(8)
GPIO9 = const(9)
GPIO10 = const(10)
GPIO11 = const(11)
