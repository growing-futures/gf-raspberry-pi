from gpiozero import Button

#BUTTONS
UpPin = 6
DownPin = 13
SetPin = 19
LoadPin = 26

UpButton = Button(UpPin)
DownButton = Button(DownPin)
SetButton = Button(SetPin)
LoadButton = Button(LoadPin)

UpPressed = False
DownPressed = False
SetPressed = False
LoadPressed = False
ButtonPressed = False

def UpButtonPressed():
	global UpPressed
	UpPressed = True
def DownButtonPressed():
	global DownPressed
	DownPressed = True
def SetButtonPressed():
	global SetPressed
	SetPressed = True
def LoadButtonPressed():
	global LoadPressed
	LoadPressed = True
def UpdateButtonPressed():
	if UpPressed or DownPressed or SetPressed or LoadPressed:
		global ButtonPressed
		ButtonPressed = True
def ResetButtons():
	global UpPressed
	global DownPressed
	global SetPressed
	global LoadPressed
	global ButtonPressed
	UpPressed = False
	DownPressed = False
	SetPressed = False
	LoadPressed = False
	ButtonPressed = False
	
UpButton.when_pressed = UpButtonPressed
DownButton.when_pressed = DownButtonPressed
SetButton.when_pressed = SetButtonPressed
LoadButton.when_pressed = LoadButtonPressed