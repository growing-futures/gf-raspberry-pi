from influxdb import InfluxDBClient

hostName = '34.234.172.6'
hostPort = 8086
dbname = 'testdb'


client = InfluxDBClient(host=hostName, port=hostPort)

jsonBody = """[
	{
		"measurements": "TowerData",
		"tags": {
			"towerName": "myTestTower",
			"towerGroup": "myTestGroup"
		},

		"fields": {
			"water_level": 0.0,
			"pH": 0.0,
			"light_sensor": "off"
		}
	}
]"""

client.create_database(dbname)

client.switch_database(dbname)

if client.write_points(jsonBody):
    print "Insert success"
