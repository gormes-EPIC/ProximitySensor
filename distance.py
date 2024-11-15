import time
import board
import adafruit_hcsr04
import digitalio

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D18, echo_pin=board.D12)

green = digitalio.DigitalInOut(board.D6)
yellow = digitalio.DigitalInOut(board.D13)
red = digitalio.DigitalInOut(board.D19)

green.direction = digitalio.Direction.OUTPUT
yellow.direction = digitalio.Direction.OUTPUT
red.direction = digitalio.Direction.OUTPUT

green.value = False
yellow.value = False
red.value = False

while True:
	try:
		dist = sonar.distance
		print(dist)
		if dist < 10:
			green.value = False
			yellow.value = False
			red.value = True
		elif dist < 20 and dist > 10:
			green.value = False
			red.value = False
			yellow.value = True
		else:
			red.value = False
			yellow.value = False
			green.value = True
	except RuntimeError:
		print("Retrying!")
	time.sleep(2)
