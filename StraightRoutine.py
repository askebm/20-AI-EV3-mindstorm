#!/usr/bin/python3.4

import ev3dev.ev3 as ev3
from time import sleep
from pybricks.robotics import DriveBase

import signal


btn = ev3.Button()

mA = ev3.LargeMotor('outA')
mB = ev3.LargeMotor('outB')

THRESHOLD_LEFT = 30

BASE_SPEED = 30
TURN_SPEED = 80

# confirm this is the correct inputs 
color1 = ev3.ColorSensor('in1')
color2 = ev3.ColorSensor('in2') 

TouchSensor = ev3.TouchSensor('in4')

color1.mode = 'COL-COLOR'

assert color1.connected, "LightSensorLeft(ColorSensor) is not connected"
assert color2.connected, "LightSensorRight(ColorSensor) is not connected"

assert TouchSensor.connected, "Touch sensor is not connected"

colors = ('unknown','black','blue','green', 'yellow', 'red', 'white', 'brown')

mB.run_direct()
mA.run_direct()


mA.polarity = "inversed"
mB.polarity = "inversed"

# EV3 Micropython 2.0
robot = DriveBase(mA, mB, wheel_diameter=55.5, axle_track=104)

def signal_handler(sig, frame):
	print('Shutting down gracefully')
	mA.duty_cycle_sp = 0
	mB.duty_cycle_sp = 0

	exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit')

# if cross target is 0 we expect an action different than going straight when seeing the next cross
# Controller should be able to set cross_target
cross_target = 0

previousColor1Value = 0
previousColor2Value = 0

def cross_detection():
	# increment counter
	global cross_target

	# we should hold onto the last reported values from the color sensors.
	# if the last value was lower than threshold we didn't see the cross previously. 
	# if then the current value is greater than threshold we have seen a cross and should increment
	# maybe we should wait with incrementing until we see lower than threshold again to confirm
	# we are past a cross
	# if the previous color sensor values were greater than threshold and the current
	# are lower than threshold we have moved past a cross.
	if color1.value() and color2.value() > THRESHOLD_LEFT:
		if cross_target == 2:
			# stop
			mA.duty_cycle_sp = 0
			mB.duty_cycle_sp = 0
			# rotate etc etc.

			#reset cross_target
			cross_target = 0
		else:
			# haven't reached the target amount of crosses
			cross_target = cross_target + 1

while True:
	sensorLeft = color1.value()
	sensorRight = color2.value()

	mA.duty_cycle_sp = BASE_SPEED
	mB.duty_cycle_sp = BASE_SPEED
	tou_val = TouchSensor.value()

	if tou_val == 1:
		ev3.Sound.beep().wait()
		mA.duty_cycle_sp = 0
		mB.duty_cycle_sp = 0
		exit()
	else:
		print(colors[color1.value()])
		print("Color sensor value: ", tou_val)
	
	cross_detection()

	previousColor1Value = sensorLeft
	previousColor2Value = sensorRight
