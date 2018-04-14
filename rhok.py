import serial
import time

# Use this cmd to get the dev name of the arduino
# ls /dev/tty*
ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    sensor_data = ser.readline()
    # Convert byte array to a string.
    sensor_data = str(sensor_data).split(',')
    print(sensor_data)
    #time.sleep(0.5)
