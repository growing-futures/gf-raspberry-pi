#import logging
from influxdb import InfluxDBClient
import json
#from sensor import sensor_fields
import serial  # For communication with arduino.
import time


hostName = '34.234.172.6'
hostPort = 8086
dbname = 'gf'


sensor_source = ["measurement", "tags", "fields"]

sensor_tags = [
        "towerName",
        "towerGroup"
]

sensor_fields = [
        "water_level",
        "air_humidity",
        "air_temp",
        "water_temp",
        "light_status",
        "pH"
]

sensor_fields_len = len(sensor_fields)

# Ref: https://oscarliang.com/connect-raspberry-pi-and-arduino-usb-cable/

def to_dict(sensor_data):
    # TODO - have dict already created, only need to populate with new sensor
    # data
    d = {}
    d['measurement'] = 'TowerData'

    d['tags'] = {}
    d['tags']['towerName'] = "Tower_%s" % tower_name
    d['tags']['towerGroup'] = "Tower_Group_%s" % (tower_name % 10 + 1)

    d['fields'] = {f:sensor_data[e] for e,f in enumerate(sensor_fields)}

    #d['fields'] = {}
    #d['fields']['water_level'] = float(random.choice(water_level_num))
    #d['fields']['pH'] = float(random.choice(pH))
    #d['fields']['light_sensor'] = random.choice(["off", "on"])
    return d


def main():
    # Use this cmd on the rpi to get the dev name of the arduino. There will
    # be a bunch of tty devices. It is usually something like ttyACM0
    # or ttypUSB0. The last number is dependant on the usb port being used.
    # ls /dev/tty*
    ser = serial.Serial('/dev/ttyACM1', 9600)
    client = InfluxDBClient(host=hostName, port=hostPort, username='gfsensor',
            password='rhokmonitoring')

    #sensor_dict = {f:0.0 for f in sensor_fields}

    while True:
        try:
            sensor_data = ser.readline()
        except serial.SerialException:
            # One reason this can occur is when the rpi is disconnected from the
            # arduino.
            # TODO
            #logger.error('SerialError')
            pass

        # Convert byte array to a string.
        sensor_data = sensor_data.decode('utf-8').strip().split(',')
        print(sensor_data)

        if len(sensor_fields) != sensor_fields_len:
            # TODO - error - drop data?
            continue

        # Add timestamp.
        # TODO
        #logger.info(sensor_data)

        # Output to json.
        d = [to_dict(sensor_data)]
        print(json.dumps(d))

        if client.write_points(d):
            print("Insert success")


if '__main__' == __name__:
    main()
