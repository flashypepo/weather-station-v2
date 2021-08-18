"""
config.py
device contains configuration parameters for connected sensors

2021-0816 temperature range: 18-25 (was 18-28), measurement interval=5 (was 10)
Note: do not include a sensor if not connected.
"""
import lolin_d1mini as board

# LEDS
# 2021-0817 TODO: one should be re-wired h/w
config_leds = {
    1: [board.D0, 'high_threshold'],  # red
    2: [board.D5, 'discomfort'],      # orange
    3: [board.D6, 'error'],           # yellow
    4: [board.D7, 'wifi'],            # green
    5: [board.D8, 'low_threshold'],   # blue
    6: [board.D3, 'reserve'],         # white
}
config_leds_aq = {
    1: [board.D0, 'reserve'],        # white
    2: [board.D5, 'low_threshold'],  # blue
    3: [board.D6, 'wifi'],           # green
    4: [board.D7, 'error'],          # yellow
    5: [board.D8, 'discomfort'],     # orange
    6: [board.D3, 'high_threshold'], # red
}

# configuration parameters for device
config_device = {
    'measurement_interval': 1,   # in seconds. SGP30 must be read every seconds
    'config_mode_switch_pin': board.D4,   # PP: FUTURE USE for button
}
# configuration parameters for device
config_sensors = {
    'sgp30_sensor': [board.I2C_SCL, board.I2C_SDA],
    'co2_threshold': [400, 1000],  # lowest value of sensor is 400
}
"""
# add sensors, like other sensors + threshold vlaues
# AHT10 sensor - temperature and humidty
    'aht10_sensor': [board.I2C_SCL, board.I2C_SDA],
    'temperature_interval': [18, 25],
    'discomfort' = 75
}
# DHT22 sensor:
    'dht22_sensor': board.D12,  # digital IO
    'temperature_threshold': [18, 25],
# MHZ19B - CO2 sensor
    'mhz19b_sensor': [board.Tx, board.Rx],   # UART conection
    'co2_threshold': [400, 1000],
"""