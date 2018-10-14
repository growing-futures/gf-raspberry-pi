#this will be the main code.
import time
import Arduino_I2C_Comm as AC
import Button_Interface as BI
import LCD_Interface as LI

buttonDelay = 0.4 #0.4 seconds
hourDelay = 30 #3600 seconds #changed in order to log every 30 seconds.
welcomeTimeout = 10

buttonStart = time.time()
hourStart = time.time()
welcomeStart = time.time()
welcomeShowing = False
	
def calibratePH():
	#calibrate the PH Sensor
	LI.printString("To Calibrate PH ", 1)
	LI.printString(" Re-Upload Code ",2)
	time.sleep(5)
	LI.showSensorData()
	global welcomeShowing
	welcomeShowing = False

while(1):

	#repeat every hour
	#gather new data and send it the the servers
	if time.time() > (hourStart + hourDelay):
		print("Hour Section")
		AC.getData()
		#send data
		#global hourStart
		hourStart = time.time()
	
	#repeat every 0.5 seconds(ish)
	#check the button status - time to check the buttons?
	if time.time() > (buttonStart + buttonDelay):
		BI.UpdateButtonPressed()
		if BI.ButtonPressed:
			if not welcomeShowing:
				print("Button Section")
				if BI.UpPressed or BI.DownPressed:
					#print("Arrow Pressed")
					LI.showSensorData()
					welcomeShowing = False
				elif BI.LoadPressed:
					#print("LoadPressed")
					AC.getData()
					LI.showSensorData()
					welcomeShowing = False
				elif BI.SetPressed:
					#print("SetPressed")
					calibratePH()
			else:
				LI.showSensorData()
				welcomeShowing = False
			#global buttonStart
			buttonStart = time.time()
			BI.ResetButtons()
	
	#check for welcome timeout
	if ((time.time() - buttonStart) > welcomeTimeout) and not welcomeShowing:
		print("Welcome Section")
		LI.showWelcomeScreen()
		welcomeShowing = True
