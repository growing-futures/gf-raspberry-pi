#!/usr/bin/env python
from influxdb import InfluxDBClient
import json
import random
import time

hostName = 'growingfuturesapp.ca'
hostPort = 8086
dbname = 'gf'


client = InfluxDBClient(host=hostName, port=hostPort, username='gfsensor', password='rhokmonitoring', ssl=True)
#client = InfluxDBClient(host=hostName, port=hostPort, username='gfsensor', password='rhokmonitoring')

json_string = """[
    {"measurement": "TowerData",
    "tags": {
        "towerName": "Tower_%s",
        "towerGroup": "Tower_Group_%s"
        },

        "fields": {
            "water_level": %f,
            "pH": %.1f,
            "light_sensor": "%s"
        }



    }]"""

tower_name_num = range(1,51)
tower_group_num = range(1,11)
water_level_num = range(1, 101)
pH = [float(x)/10 for x in range(150)]
light_sensor = "off";

client.switch_database(dbname)

while True:
    time.sleep(0.02)
    tower_name = random.choice(tower_name_num)

    d = {}
    d['measurement'] = 'TowerData'
    d['tags'] = {}
    d['tags']['towerName'] = "Tower_%s" % tower_name
    d['tags']['towerGroup'] = "Tower_Group_%s" % (tower_name % 10 + 1)
    d['fields'] = {}
    d['fields']['water_level'] = float(random.choice(water_level_num))
    d['fields']['pH'] = float(random.choice(pH))
    d['fields']['light_sensor'] = random.choice([0, 1, 2, 3]) 
    d['fields']['flow_status'] = float(random.choice(range(0,11)))

    if client.write_points([d]):
        print "Insert success"
