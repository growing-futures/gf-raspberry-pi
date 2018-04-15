#import logging
from enum import Enum, unique
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
import json
#from sensor import sensor_fields
import serial  # For communication with arduino.
import time


MEASUREMENT = 'measurement'
TAGS = 'tags'
DB = 'db'
ARDUINO = 'arduino'
CONFIG_KEYS = (MEASUREMENT, TAGS, DB, ARDUINO)
#CONFIG_KEYS = (MEASUREMENT, TAGS, FIELDS, DB, ARDUINO)

FIELDS = 'fields'

F_WATER_LEVEL = "water_level"
F_AIR_HUMIDITY = "air_humidity"
F_AIR_TEMP = "air_temp"
F_WATER_TEMP = "water_temp"
F_PH = "pH"
F_LIGHT_STATUS_1 = "light_status_1"
F_LIGHT_STATUS_2 = "light_status_2"
F_LIGHT_STATUS_3 = "light_status_3"
F_LIGHT_STATUS_4 = "light_status_4"



WL = "water_level"
WL_SENSOR_HEIGHT = "sensor_height"
WL_MAX = "max_water_level"
WL_MIN = "min_water_level"


@unique
class LightStatus(Enum):
    on  = 1
    off = 2
    on_expected  = 3  # light is off, but it should be on
    off_expected = 4  # light is on, but it should be off


def to_float(s):
    try:
        return float(s)
    except ValueError:
        # TODO
        return s


def to_str(s): return s


def to_light_status(light_data):
    """Used to convert light sensor data to light status."""
    # TODO - convert to enum
    if 1 == light_data: status = LightStatus.on
    else: status =  LightStatus.off
    return to_float(status.value)


def create_to_water_level(config_data):
    """Used to create the 'to_water_level' func."""
    wl_config = config_data[WL]
    def to_water_level(sensor_value, height=wl_config[WL_SENSOR_HEIGHT],
            wl_max=wl_config[WL_MAX], wl_min=wl_config[WL_MIN]):
        sensor_value = to_float(sensor_value)
        print(height, wl_max, wl_min, sensor_value)
        return (height - sensor_value - wl_min / (wl_max - wl_min)) * 100
    return to_water_level


# Required as the arduino sends us the data in this order.
FIELD_ORDER = (
        F_WATER_LEVEL,
        F_AIR_HUMIDITY,
        F_AIR_TEMP,
        F_WATER_TEMP,
        F_PH,
        F_LIGHT_STATUS_1,
        F_LIGHT_STATUS_2,
        F_LIGHT_STATUS_3,
        F_LIGHT_STATUS_4,
)

FIELDS_LEN = len(FIELD_ORDER)



def to_dict(config_data, field_dict, sensor_data):
    """Used to convert the sensor data into a dict for easy conversion to
    json format.
    """
    # TODO - have dict already created, only need to populate with new sensor
    # data
    d = {}

    # Measurement data.
    d[MEASUREMENT] = config_data[MEASUREMENT]
    d[TAGS] = dict(config_data[TAGS])

    fields = {}

    for e, field in enumerate(FIELD_ORDER):
        # We ignore 'x' fields. The arduino is sending 4 light statuses even
        # if they only have 1 light. We filter out any that don't have data.
        convert_func = field_dict.get(field, to_str)
        data = sensor_data[e]
        if 'x' == data: continue
        fields[field] = convert_func(data)

    d[FIELDS] = fields
    return d


def get_config_data(filename):
    """Used to read the json config data."""
    with open(filename) as fp:
        config_data = json.load(fp)

    # Do some basic checking.
    for key in CONFIG_KEYS:
        if key not in config_data:
            print('ERROR: Missing config.json key "{}"'.format(key))
    return config_data


def main():
    # Use this cmd on the rpi to get the dev name of the arduino. There will
    # be a bunch of tty devices. It is usually something like ttyACM0
    # or ttypUSB0. The last number is dependant on the usb port being used.
    # ls /dev/tty*
    ser = serial.Serial('/dev/ttyACM1', baud_rate)
    client = InfluxDBClient(host=host_name, port=host_port, username='gfsensor',
            password='rhokmonitoring', ssl=True, verify_ssl=True)
    client.switch_database(dbname)

    # Read in the config data.
    config_data = get_config_data(CONFIG_FILENAME)
    print(config_data)

    field_dict = {
            F_WATER_LEVEL : create_to_water_level(config_data),
            F_AIR_HUMIDITY : to_float,
            F_AIR_TEMP : to_float,
            F_WATER_TEMP : to_float,
            F_PH : to_float,
            F_LIGHT_STATUS_1 : to_light_status,
            F_LIGHT_STATUS_2 : to_light_status,
            F_LIGHT_STATUS_3 : to_light_status,
            F_LIGHT_STATUS_4 : to_light_status,
    }

    while True:
        try:
            sensor_data = ser.readline()
        except serial.SerialException as e:
            # One reason this can occur is when the rpi is disconnected from the
            # arduino.
            # TODO
            print('Exception: {}'.format(e))
            break

        # Convert byte array to a string.
        sensor_data = sensor_data.decode('utf-8').strip().split(',')
        #print(sensor_data)

        if len(sensor_data) != FIELDS_LEN:
            # TODO - error - drop data?
            print('WARNING: Sensor data length mismatch (ignoring sensor '
                    'data), received {} values, expecting {} values'.format(
                    len(sensor_data), sensor_fields_len))
            continue

        # Add timestamp.
        # TODO
        #logger.info(sensor_data)

        # Output to json.
        d = [to_dict(config_data, field_dict, sensor_data)]
        print(json.dumps(d))

        try:
            if not client.write_points(d):
                print('Failed client data write: {}'.format(d))
        except InfluxDBClientError as e:
            print('Exception: {}'.format(e))


if '__main__' == __name__:
    main()
