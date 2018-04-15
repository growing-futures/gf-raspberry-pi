import smbus
import time
bus = smbus.SMBus(1)
address = 0x8

def querySensor(address, cmd):
    try:
        sensor_data = bus.read_i2c_block_data(address, cmd)
    except OSError as e:
        print(e)
    sensor_string = ""
    for charbyte in sensor_data:
        if charbyte == 255:
            break
        sensor_string += chr(charbyte)
    time.sleep(0.2)
    print(sensor_data)
    return sensor_string

while True:
    waterLevel = querySensor(address, 1)
    airHumidity = querySensor(address, 2)
    airTemperature = querySensor(address, 3)
    waterTemperature = querySensor(address, 4)
    pH = querySensor(address, 5)
    lightStatus = querySensor(address, 6)

    print("Water Level: " + waterLevel)
    print("Air Humidity: " + airHumidity)
    print("Air Temperature: " + airTemperature)
    print("Water Temperature: " + waterTemperature)
    print("pH: " + pH)
    print("Light Status: " + lightStatus)

    time.sleep(1)
