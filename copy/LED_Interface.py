#LED Control
from gpiozero import LED
import ThresholdConfig as TC

red = LED(16)
green = LED(20)

def redOn():
	red.on()
def redOff():
	red.off()
def greenOn():
	green.on()
def greenOff():
	green.off()

def checkTower():
	redOn()
	greenOff()
	
def allGood():
	redOff()
	greenOn()
	
def updateLEDStatus(list):
	if (float(list[0]) < TC.LOW_WATER_LEVEL_THRESHOLD):
		checkTower()
	elif float(list[1]) < TC.LOW_WATER_FLOW_THRESHOLD:
		checkTower()
	elif float(list[2]) < TC.LOW_PH_THRESHOLD:
		checkTower()
	elif float(list[2]) > TC.HIGH_PH_THRESHOLD:
		checkTower()
	else:
		allGood()
		
redOff()
greenOff()
