##########################################################################
# Random Hacks of Kindness - 2018 April 13-15
# Project #1 - Growing Futures Hydroponic Monitoring System
# https://rhok.ca/events/rhok-8/
#
# This code is used to read data from an arduino, clean it up a bit and then
# put it in a database.
#
# Currently all our code is in one file for easy of updating. In the future
# it would be nice to have this split over separate files.
#
##########################################################################
# Requirements:
# -python 3
# -library: pySerial - http://pyserial.readthedocs.io
# -library: InfluxDBClient - https://pypi.python.org/pypi/influxdb
# -correct system time (for light's status)
#
##########################################################################
# Usage:
# Run the script. This can be used to change the configuration data and/or
# loop on the sensor data.
# >>> python3 rhok.py
#
# Used to skip the setup.
# >>> python3 rhok.py --skip_setup
#
##########################################################################
# Notes:
# If a json dictionary key string is changed in the configuration file, the
# string also needs to be changed in this file.
#
# Example configuration file entry:
# "tags" : {
#     "towerName" : "Tower_60",
#     "towerGroup" : "Tower 60 Postal Office"
# }
#
# If a string key name ("tags", "towerName", or "towerGroup") is changed in
# the configuration file, its corresponding value in this file needs to be
# updated.
#
# TAGS = 'tags'
# T_TOWER_NAME = "towerName"
# T_TOWER_GROUP = "towerGroup"
#
# If a value is changed (eg. from above: "Tower_60" or
# "Tower 60 Postal Office"), that does not need to be reflected in this file.
#
##########################################################################
# Example of the data format that is written to influxdb.
# [{
#       "measurement" : "TowerData",
#
#       "tags" : {
#           "towerName" : "Tower_60",
#           "towerGroup" : "Tower 60 Postal Office"
#       },
#
#       "fields" : {
#           "water_level" : 80.5,
#           "air_humidity" : 44.4,
#           "air_temp" : 25.2,
#           "water_temp" : 22.9,
#           "pH" : 7.0,
#       }
# }]
##########################################################################


from datetime import datetime, time
from enum import Enum, unique
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
import json
import sys


# This is our default config file. Don't write to this. Read only.
DFLT_CONFIG_FILENAME = 'default_config.json'
CONFIG_FILENAME = 'config.json'

# Most of the following consts are based on the strings in the config.json
# file.
MEASUREMENT = 'measurement'

TAGS = 'tags'
T_TOWER_NAME = "towerName"
T_TOWER_GROUP = "towerGroup"

TAGS_ORDER = (
        T_TOWER_NAME,
        T_TOWER_GROUP,
)

DB = 'db'
DB_HOST_NAME = "host_name"
DB_HOST_PORT = "host_port"
DB_DBNAME = "dbname"
DB_USERNAME = "username"

DB_ORDER = (
        DB_HOST_NAME,
        DB_HOST_PORT,
        DB_DBNAME,
        DB_USERNAME,
)


ARDUINO = 'arduino'
A_BAUD_RATE = 'baud_rate'

WATER_LEVEL = 'water_level'
WL_SENSOR_HEIGHT = "sensor_height"
WL_MAX = "max_water_level"
WL_MIN = "min_water_level"

WATER_LEVEL_ORDER = (
        WL_SENSOR_HEIGHT,
        WL_MAX,
        WL_MIN,
)

# Used with the light sensor code.
ARDUINO_LIGHT_ON = 1
ARDUINO_INVALID_DATA = 'x'

# Used to validate light sensor hour/minute values.
MIN_HOUR = 0
MAX_HOUR = 23
MIN_MINUTE = 0
MAX_MINUTE = 59


CONFIG_KEYS = (MEASUREMENT, TAGS, DB, ARDUINO, WATER_LEVEL)
SETUP_KEYS = (TAGS, DB, WATER_LEVEL)

# This is used to keep the setup order consistant over each setup.
SETUP_KEYS_ORDER_DICT = {
        TAGS : TAGS_ORDER,
        DB : DB_ORDER,
        WATER_LEVEL : WATER_LEVEL_ORDER,
}


FIELDS = 'fields'
F_WATER_LEVEL = "water_level"
F_FLOW_STATUS = "flow_status"
F_AIR_HUMIDITY = "air_humidity"
F_AIR_TEMP = "air_temp"
F_WATER_TEMP = "water_temp"
F_PH = "pH"


# Required as the arduino sends us the data in this order.
FIELD_ORDER = (
        F_WATER_LEVEL,
        F_FLOW_STATUS,
        F_PH,
)

FIELDS_LEN = len(FIELD_ORDER)

# Ref: https://stackoverflow.com/a/10748024
def time_in_range(start, end, in_time):
    """Return True if in_time is in the range [start, end]"""
    if start <= end:
        return start <= in_time <= end
    else:
        return start <= in_time or in_time <= end


def to_float(s):
    try:
        return float(s)
    except ValueError:
        # Re-raise the exception, to be caught by users of this function.
        raise e


def to_int(s):
    try:
        return int(s)
    except ValueError:
        # Re-raise the exception, to be caught by users of this function.
        raise e


def to_str(s): return s


def create_to_water_level(config_data):
    """Used to create the 'to_water_level' func."""
    wl_config = config_data[WATER_LEVEL]
    height = wl_config[WL_SENSOR_HEIGHT]
    wl_max = wl_config[WL_MAX]
    wl_min = wl_config[WL_MIN]
    wl_diff = wl_max - wl_min

    def to_water_level(sensor_value, height=height, wl_min=wl_min,
            wl_diff=wl_diff):
        return ((height - to_float(sensor_value) - wl_min) / wl_diff) * 100
    return to_water_level


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
        convert_func = field_dict.get(field, to_str)
        data = sensor_data[e]
        if ARDUINO_INVALID_DATA == data: continue

        try:
            fields[field] = convert_func(data)
        except ValueError as e:
            # Skip this field/data. This is most likely caused by a sensor
            # value not being as expected (ie. to_int or to_float)
            print('Exception: {}'.format(e))
            continue

    d[FIELDS] = fields
    return d


def check_config_data_keys_sanity(config_data):
    """Does very basic sanity on the config data keys."""
    for key in CONFIG_KEYS:
        if key not in config_data:
            print('ERROR: Missing config file key "{}"'.format(key))
            return False
    return True


def get_config_data(filename):
    """Used to read the json config data."""
    try:
        with open(filename) as fp:
            config_data = json.load(fp)
    except OSError as e:
        print('Exception: {}'.format(e))
        print('ERROR: Unable to read config file: {}'.format(filename))
        return {}

    if check_config_data_keys_sanity(config_data): return config_data
    else: return {}


def update_config_data(filename, config_data):
    """Used to overwrite the json config data."""
    if not check_config_data_keys_sanity(config_data):
        print('ERROR: Invalid config data={}, config file not updated'.format(
            config_data))
        return False

    try:
        with open(filename, 'w') as fp:
            json.dump(config_data, fp, indent=4)
            #print(json.dumps(config_data))
    except OSError as e:
        print('Exception: {}'.format(e))
        print('ERROR: Unable to write config file: {}'.format(filename))
        return False
    return True


def create_sensor_field_dict(config_data):
    return {
            F_WATER_LEVEL : create_to_water_level(config_data),
            F_AIR_HUMIDITY : to_float,
            F_AIR_TEMP : to_float,
            F_WATER_TEMP : to_float,
            F_FLOW_STATUS : to_float,
            F_PH : to_float,
    }

def config_db_client(config_data):
    try:
        # TODO - remove password
        db = config_data[DB]
        client = InfluxDBClient(host=db[DB_HOST_NAME], port=db[DB_HOST_PORT],
                username=db[DB_USERNAME], password='GfSensorP@ssw0rd!@#', ssl=True,
                verify_ssl=True)
        client.switch_database(db[DB_DBNAME])
        return client
    except InfluxDBClientError as e:
        print('Exception: {}'.format(e))
        print('ERROR: Unable to configure influx db client: host={}, port={}, '
            'username={}'.format(
                db[DB_HOST_NAME], db[DB_HOST_PORT], db[DB_USERNAME]))
        return None

def send_data(data_list):
	"""Does some initial config then loops forever reading the sensor data."""
	config_data = get_config_data(CONFIG_FILENAME)
        if not config_data: return

        field_dict = create_sensor_field_dict(config_data)

        db_client = config_db_client(config_data)
        if db_client is None: return

        # Convert byte array to a string. Common separated values.

        if len(data_list) != FIELDS_LEN:
            # This can happen once in while, especially during the first few
            # reads.
            print('WARNING: Sensor data length mismatch (ignoring sensor '
                    'data), received {} values, expecting {} values'.format(
                    len(data_list), FIELDS_LEN))
            return 

        # Output to json.
        d = [to_dict(config_data, field_dict, data_list)]
        print(json.dumps(d))

        try:
            if db_client.write_points(d):
                print('DB updated with data: {}'.format(d))
            else:
                print('Failed db client data write: {}'.format(d))
        except InfluxDBClientError as e:
            print('Exception: {}'.format(e))
            print('ERROR: Unable to write data to client db, data={}'.format(d))

if '__main__' == __name__:
    main()

