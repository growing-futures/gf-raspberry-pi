from smbus import SMBus
import time

bus = SMBus(1)
slaveAddress = 0x12
data_rfA = ""
#delayTime = 15

def log(data):
	logfile = open('/home/pi/logTest2.txt','a+')
	logfile.write(data)
	logfile.write('\n')
	logfile.close()
	
def getData():
	global data_rfA
	try:
		print("Trying to read")
		x = bus.read_byte(slaveAddress) #is new data ready?
		if(x == 1):
			bus.write_byte(slaveAddress, 1) #request new data to be sent
			time.sleep(5) #give the Arduino time to prepare data
			#read 30 characters from Arduino
			data_rfA = bus.read_i2c_block_data(slaveAddress, 0 ,30)
			data_rfA = ''.join(chr(i) for i in data_rfA)
			print(data_rfA)
			#log(data_rfA)
			data_rfA = data_rfA.strip().split(',')
			print("data_rfA split: " + str(data_rfA))
			bus.write_byte(slaveAddress, 3)
	except IOError:
		#data_rfA = "IOError"
		print "IOError Get"
		time.sleep(1) #let the Arudino reset if necessary or gather new data

def sendData(data):
	try:
		print("Trying to read")
		bus.write_byte(slaveAddress, 4) #is new data ready?
		time.sleep(5)
		x = bus.read_byte(slaveAddress)
		print("Bus Read")
		if(x == 4):
			print(x)
			while (len(data) < 30):
				data = data + " "
			bus.write_i2c_block_data(slaveAddress, " ", data) #request new data to be sent
			time.sleep(5) #give the Arduino time to prepare data
			
			
			#read 30 characters from Arduino
			data_rfA = bus.read_i2c_block_data(slaveAddress, 0 ,30)
			print(data_rfA)
			data_rfA = ''.join(chr(i) for i in data_rfA)
			print(data_rfA)
			log(data_rfA)
			bus.write_byte(slaveAddress, 3)
	except IOError:
		#data_rfA = "IOError"
		print "IOError Send"
		raise e
		time.sleep(1) #let the Arudino reset if necessary or gather new data
		
#while(1):
	#time.sleep(1)
	#getData()
