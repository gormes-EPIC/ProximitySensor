# Proximity Stoplight

## Overview

This project takes input from a distance sensor turns on a different colored lights based on how close the object is.

![cover_image](https://github.com/user-attachments/assets/e7dbec0f-edd4-40b0-9e0b-83736fab1000)

If the object is closer than 10 cm, the red light turns on. If the object is between 10 and 20 cm the yellow light turns on. And anything farther than 20 cm the green light will turn on. The distance is found using an ultrasonic distance sensor. The stoplight automatically starts when the Pi is turned on. 

## How To Build

### Materials

1. Raspberry Pi
2. T-Cobbler
3. Breadboard
4. M-M jumper wires
5. HY-SRF05 Ultrasonic Distance Sensor
6. KS0310 Keyestudio Traffic Light Module
7. (2)100 k$\Omega$ resistor 
### Build the Circuit

![circuit_diagram](https://github.com/user-attachments/assets/aa68bb97-de90-4432-9c80-23859a781d29)

##### Wiring the Ultrasonic Distance Sensor

![ultrasonic_wiriing](https://github.com/user-attachments/assets/49899f6c-eca9-47e8-8909-8a74f9290103)

[Original Image Source](https://jawhersebai.com/tutorials/how-to-use-the-hy-srf05-ultrasonic-distance-sensor/)

Connect the following pins:
- **VCC** to **5V**
- **Trig** to **GPIO**
- **Echo** to **GPIO** and **Ground** through **100k$\Omega$ resistors**
- **GND** to **Ground**

The HC-SR04 uses 5V logic, so you will have to use a level shifter or simple voltage divider to use it with your sensor. That's why you need to add resistors to your Echo pin. 

Refer to [Adafruit](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython) for more information about wiring.

#### Wiring the Stoplight

![stoplight_wiring|400](https://github.com/user-attachments/assets/8d068f78-eaa5-4d9f-98a8-35fee5626145)

[Original Image Source](https://wiki.keyestudio.com/KS0310_Keyestudio_Traffic_Light_Module_(Black_and_Eco-friendly))

Connect the following pins:
- **R** to **GPIO**
- **Y** to **GPIO**
- **G** to **GPIO**
- **GND** to **Ground**

## Writing the Code

Install the CircuitPython HC-SR04 library:

```
pip3 install adafruit-circuitpython-hcsr04
```

See these links for more information: 
- [Adafruit HCSRO4 wiring and libraries](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython) 
- [Adafruit HCSRO4 on GitHub](https://github.com/adafruit/Adafruit_CircuitPython_HCSR04) 
- [Adafruit HCSRO4 Library Docs](https://docs.circuitpython.org/projects/hcsr04/en/stable/api.html)

Create a program `distance.py`: 

```python
import time
import board
import adafruit_hcsr04
import digitalio

# Detect and create a HCSRO4 object on trigger pin 18 and echo pin 12 
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D18, echo_pin=board.D12)

# Define the R, Y, and G pins as DigitialInOut objects
green = digitalio.DigitalInOut(board.D6)
yellow = digitalio.DigitalInOut(board.D13)
red = digitalio.DigitalInOut(board.D19)

# Set the R, Y, and G pins as outputs 
green.direction = digitalio.Direction.OUTPUT
yellow.direction = digitalio.Direction.OUTPUT
red.direction = digitalio.Direction.OUTPUT

# Set their current state to false to start
green.value = False
yellow.value = False
red.value = False

# While the program is running
while True:
	try:
		dist = sonar.distance # Try to get the distance from the sensor
		print(dist)
		if dist < 10: # If the distance is less than 10, turn on red
			green.value = False
			yellow.value = False
			red.value = True
		elif dist < 20 and dist > 10: # If the distance is between 10 and 20, turn on yellow 
			green.value = False
			red.value = False
			yellow.value = True
		else: # If the distance is more than 20, turn on green
			red.value = False
			yellow.value = False
			green.value = True
	except RuntimeError: # If the sensor fails, don't stop the program
		print("Retrying!")
	time.sleep(2) # Wait 2 seconds between readings
```

Refer to [Digital I/O with Circuit Python](https://learn.adafruit.com/adafruit-io-basics-digital-output?view=all#python-wiring) and [Adafruit HCSRO4 wiring and libraries](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython).  

## Schedule a cron Job

To set up the program to run automatically when the Pi turns on, we need to schedule a `cron` job.

To create a job, edit the `crontab`  file with `crontab -e`.

Then, add the following line to the bottom of the file:

```
@reboot /path/to/python3 -c /path/to/distance.py
```

This will run your `distance.py` using `python3` on every reboot of the Pi.

## Testing your project

When you run your program, your project should perform like the following video and print the readings from the ultrasonic distance sensor to the terminal.

![[https://github.com/user-attachments/assets/75422577-b82d-4005-b618-e8c20dae871f]]


## References

- [Keyestudio Traffic Light Module](https://wiki.keyestudio.com/KS0310_Keyestudio_Traffic_Light_Module_(Black_and_Eco-friendly))
- [Python Wiring and Digital I/O with Circuit Python](https://learn.adafruit.com/adafruit-io-basics-digital-output?view=all#python-wiring)
- [Adafruit HCSRO4 wiring and libraries](https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython) 
- [Adafruit HCSRO4 on GitHub](https://github.com/adafruit/Adafruit_CircuitPython_HCSR04) 
- [Adafruit HCSRO4 Library Docs](https://docs.circuitpython.org/projects/hcsr04/en/stable/api.html)
