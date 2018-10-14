#LCD and button control.
import RPi_I2C_driver #RPi_I2C_driver: https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
from time import *

LCD = RPi_I2C_driver.lcd()

#LCD.lcd_display_string("TEXT", LINE) #line = 1 or 2
#LCD.lcd_display_string_pos("TEXT", LINE, COL) #line 1-2, COL - 0-15
#LCD.lcd_clear() #clears the display

## Settings ##
def showHostname():
    with open('/etc/hostname', 'r') as f:    
        hostname =  f.readline()
    
    LCD.lcd_clear()
    LCD.lcd_display_string("Hostname: ",1)
    LCD.lcd_display_string(hostname,2)

def showCalibration():
    LCD.lcd_clear()
    LCD.lcd_display_string("Calibrate?",1)
    LCD.lcd_display_string("Press settings button again",2)    

## END:Settings ##    

## Sensors ##
def showWaterLevel(waterLevel):    
    LCD.lcd_clear()
    LCD.lcd_display_string("Water Level:",1)
    LCD.lcd_display_string(waterLevel,2)

def showPumpFlow(pumpFlow):
    LCD.lcd_clear()
    LCD.lcd_display_string("Pump Flow:", 1)
    LCD.lcd_display_string(pumpFlow, 2)
    
def showpH(pH):
    LCD.lcd_clear()
    LCD.lcd_display_string("pH: ",1)
    LCD.lcd_display_string_pos(pH, 1, 4)

def showWelcomeScreen():
    LCD.lcd_clear()
    LCD.lcd_display_string("   Welcome To   ",1)
    LCD.lcd_display_string("GROWING FUTURES!",2)

def showRestartingScreen():
	LCD.lcd_clear()
	LCD.lcd_display_string("    RESETING    ",1)
	LCD.lcd_display_string("     LET GO     ",2)

def showCollectingScreen():
	LCD.lcd_clear()
	LCD.lcd_display_string("   COLLECTING   ",1)
	LCD.lcd_display_string("      DATA      ",2)

def showRestartedScreen():
	LCD.lcd_clear()
	LCD.lcd_display_string("    RESETING    ",1)
	LCD.lcd_display_string("    COMPLETE    ",2)

def readError():
    LCD.lcd_clear()
    LCD.lcd_display_string("   READ ERROR   ",1)
    LCD.lcd_display_string("   RESET NOW!   ",2)

def printString(text, line=1):
	LCD.lcd_display_string(text, line)
	
def clearLCD():
	LCD.lcd_clear()

clearLCD()
showWelcomeScreen()
