#LCD and button control.
import RPi_I2C_driver #RPi_I2C_driver: https://gist.github.com/DenisFromHR/cc863375a6e19dce359d
from time import *

LCD = RPi_I2C_driver.lcd()

#LCD.lcd_display_string("TEXT", LINE) #line = 1 or 2
#LCD.lcd_display_string_pos("TEXT", LINE, COL) #line 1-2, COL - 0-15
#LCD.lcd_clear() #clears the display

def showWelcomeScreen():
	LCD.lcd_display_string("   Welcome To   ",1)
	LCD.lcd_display_string("GROWING FUTURES!",2)

def showSensorData(list):
	LCD.lcd_clear()
	LCD.lcd_display_string("WL: " + list[0],1)
	LCD.lcd_display_string_pos("FR: " + list[1],1,8)
	LCD.lcd_display_string("PH: " + list[2],2)
	
	#LCD.lcd_display_string("     SENSOR     ",1)
	#LCD.lcd_display_string("      DATA      ",2)

def printString(text, line=1):
	LCD.lcd_display_string(text, line)
	
def clearLCD():
	LCD.lcd_clear()

clearLCD()
showWelcomeScreen()