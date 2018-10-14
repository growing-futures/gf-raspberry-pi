from smbus import SMBus
import time

bus = SMBus(1)
slaveAddress = 0x12
data_received_from_Arduino = ""
delayTime = 15

while(1):
	time.sleep(delayTime)
	try:
		x = bus.read_byte(slaveAddress) #is new data ready?
		if (x == 1):
			#print(x)
			bus.write_byte(slaveAddress,1) #request the new  data
			time.sleep(10) #this delay can be as long as needed - give it a minute of two to gather data
			data_received_from_Arduino = bus.read_i2c_block_data(slaveAddress, 0,30) #read the new data 12 is number of characters
			#print(data_received_from_Arduino
			data_received_from_Arduino = (''.join(chr(i) for i in data_received_from_Arduino)).strip()
			print(data_received_from_Arduino)
			bus.write_byte(slaveAddress,3)
			#print(StringToBytes(data_to_send_to_Arduino))
			#bus.write_i2c_block_data(slaveAddress, 0,StringToBytes(data_to_send_to_Arduino))
	except IOError:
		print "IOError"
		time.sleep(10) #let the Arduino reboot
