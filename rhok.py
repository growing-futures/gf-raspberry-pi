#import logging
import serial  # For communication with arduino.


# Ref: https://oscarliang.com/connect-raspberry-pi-and-arduino-usb-cable/


def main_loop():
    # Use this cmd on the rpi to get the dev name of the arduino. There will
    # be a bunch of tty devices. It is usually something like ttyACM0. The last
    # number is dependant on the usb port being used.
    # ls /dev/tty*
    ser = serial.Serial('/dev/ttyUSB0', 9600)

    while True:
        try:
            sensor_data = ser.readline()
        except serial.SerialError:
            # One reason this can occur is when the rpi is disconnected from the
            # arduino.
            # TODO
            #logger.error('SerialError')
            pass

        # Convert byte array to a string.
        sensor_data = sensor_data.decode('utf-8').split(',')
        print(sensor_data)

        # Add timestamp.
        # TODO
        #logger.info(sensor_data)

        # Output to json.
        # TODO


if '__main__' == __name__:
    main_loop()
