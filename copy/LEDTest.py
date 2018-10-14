#LEDTest
from gpiozero import LED
from signal import pause

red = LED(16)
green = LED(20)

red.blink()
green.blink()

pause()
