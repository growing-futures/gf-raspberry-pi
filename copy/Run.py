#/usr/bin/python
#this will be the main code.
import time
import Arduino_I2C_Comm as AC
import Button_Interface as BI
import LCD_Interface as LI
import LED_Interface as LEDI
import rhok_lib as TR
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

buttonDelay = 0.4 #0.4 seconds
hourDelay = 3 #3600 seconds #changed in order to log every 30 seconds.
welcomeTimeout = 10
buttonStart = time.time()
hourStart = time.time()
isSensorScreen = True
isFresh = True

SensorIndex = 0
SettingIndex = 0

SensorScreens = [0, 1, 2]
SettingScreens = [0, 1]

sensor_data = ""

def manual_read():
    LI.clearLCD()
    LI.printString(" TAKING  MANUAL ", 1)
    LI.printString("     SAMPLE     ",2)
    AC.getData()
    sensor_data = AC.data_rfA

def arduino_reset():
    print("RESET START - LET GO")
    LI.showRestartingScreen()
    time.sleep(2)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, 0)
    GPIO.setup(27, GPIO.IN)
    LI.showRestartedScreen()
    time.sleep(2)
    print("RESET")
    isFresh = True

def calibratePH():
	#calibrate the PH Sensor
	LI.printString("To Calibrate PH ", 1)
	LI.printString(" Re-Upload Code ",2)
	time.sleep(5)

def CommFailure():
	time.sleep(8)

## MAIN ##
BI.ResetButtons()
LI.clearLCD()
LI.printString("    STARTING    ", 1)
LI.printString("       UP       ",2)
time.sleep(5)
arduino_reset()
time.sleep(1)
AC.getData()
sensor_data = AC.data_rfA

while(1):

    #repeat every hour
    #gather new data and send it the the servers
    if time.time() > (hourStart + hourDelay):
        try:
            LI.showCollectingScreen()
            AC.getData()
            sensor_data = AC.data_rfA
            isFresh = True
            print("Sensor data: " + str(sensor_data))
        except IOError:
            print("IOError Raised")
            CommFailure()
        #send data
        TR.send_data(sensor_data) 
        #global hourStart
        hourStart = time.time()

    #repeat every 0.5 seconds(ish)
    #check the button status - time to check the buttons?
    if time.time() > (buttonStart + buttonDelay):
        BI.UpdateButtonPressed()
        BI.LoadButton.when_held = arduino_reset
        BI.SetButton.when_held = calibratePH
        BI.DownButton.when_held = manual_read
        if BI.ButtonPressed:
            isFresh = True
            print("Button Section")
            if BI.UpPressed:
                print("Up Arrow Pressed")
                if isSensorScreen:
                    SensorIndex = SensorIndex + 1
                    SensorIndex = SensorIndex % len(SensorScreens)
                else: #SettingsScreen
                    SettingIndex = SettingIndex + 1
                    SettingIndex = SettingIndex % len(SettingScreens)
            elif BI.DownPressed:
                print("Down Arrow Pressed")
                if isSensorScreen:
                    SensorIndex = SensorIndex - 1
                    SensorIndex = SensorIndex % len(SensorScreens)
                else: #SettingsScreen
                    SettingIndex = SettingIndex - 1
                    SettingIndex = SettingIndex % len(SettingScreens)
            elif BI.LoadPressed:
                isSensorScreen = True
            elif BI.SetPressed:
                isSensorScreen = False

    if isFresh:
        if isSensorScreen:
            if SensorIndex == 0:
                try:
                    sensor_data = AC.data_rfA
                    LI.showWaterLevel(sensor_data[0])
                except:
                    LI.readError()
            if SensorIndex == 1:
                try:
                    sensor_data = AC.data_rfA
                    LI.showPumpFlow(sensor_data[1])
                except:
                    LI.readError()
            if SensorIndex == 2:
                try:
                    sensor_data = AC.data_rfA
                    LI.showpH(sensor_data[2])
                except:
                    LI.readError()
        else:
            if SettingIndex == 0:
                LI.showHostname()
            if SettingIndex == 1:
                LI.showCalibration()
        #global buttonStart
        buttonStart = time.time()
        BI.ResetButtons()
        isFresh = False

