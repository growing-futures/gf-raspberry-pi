#!/usr/bin/env python
from influxdb import InfluxDBClient
import json

hostName = '34.234.172.6'
hostPort = 8086
dbname = 'gf'


client = InfluxDBClient(host=hostName, port=hostPort, username='gfsensor', password='rhokmonitoring')

jsonBody = json.loads("""[
	{
		"measurement": "TowerData",
		"tags": {
			"towerName": "myTestTower",
			"towerGroup": "myTestGroup"
		},

		"fields": {
			"water_level": 10.0,
			"pH": 5.6,
			"light_sensor": "off"
		}
	}
]""")

client.switch_database(dbname)

if client.write_points(jsonBody):
    print "Insert success"
