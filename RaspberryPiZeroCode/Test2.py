#this will be the main code.
import time
import Arduino_I2C_Comm as AC
import Button_Interface as BI
import LCD_Interface as LI
import LED_Interface as LEDI

buttonDelay = 0.4 #0.4 seconds
hourDelay = 30 #3600 seconds #changed in order to log every 30 seconds.
welcomeTimeout = 10
buttonStart = time.time()
hourStart = time.time()
welcomeStart = time.time()
welcomeShowing = False

sensor_data = ""

def calibratePH():
	#calibrate the PH Sensor
	LI.printString("To Calibrate PH ", 1)
	LI.printString(" Re-Upload Code ",2)
	time.sleep(5)
	LI.showSensorData(sensor_data)
	global welcomeShowing
	welcomeShowing = False

def CommFailure():
	time.sleep(8)
	
while(1):

	#repeat every hour
	#gather new data and send it the the servers
	if time.time() > (hourStart + hourDelay):
		print("Hour Section")
		try:
			AC.getData()
			sensor_data = AC.data_rfA
		except IOError:
			print("IOError Raised")
			CommFailure()
		LEDI.updateLEDStatus(sensor_data)
		#send data
		#global hourStart
		hourStart = time.time()
	
	#repeat every 0.5 seconds(ish)
	#check the button status - time to check the buttons?
	if time.time() > (buttonStart + buttonDelay):
		BI.UpdateButtonPressed()
		if BI.ButtonPressed:
			if not welcomeShowing:
				#print("Button Section")
				if BI.UpPressed or BI.DownPressed:
					#print("Arrow Pressed")
					LI.showSensorData(sensor_data)
					welcomeShowing = False
				elif BI.LoadPressed:
					#print("LoadPressed")
					try:
						AC.getData()
						sensor_data = AC.data_rfA
					except IOError:
						print("IOError Raised")
						CommFailure()
					LI.showSensorData(sensor_data)
					LEDI.updateLEDStatus(sensor_data)
					welcomeShowing = False
				elif BI.SetPressed:
					#print("SetPressed")
					calibratePH()
			else:
				LI.showSensorData(sensor_data)
				welcomeShowing = False
			#global buttonStart
			buttonStart = time.time()
			BI.ResetButtons()
	
	#check for welcome timeout
	if ((time.time() - buttonStart) > welcomeTimeout) and not welcomeShowing:
		print("Welcome Section")
		LI.showWelcomeScreen()
		welcomeShowing = True