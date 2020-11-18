#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_4
from ev3dev2.sensor.lego import *
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import time

def follow_until_color(tank,sensor,color):
    if sensor.color != color:
        return True
    else:
        return False

def follow_for_distance(tank,distance):
    if not hasattr(tank, 'distance') or tank.distance is None:
        tank.left_motor.position = 0
        tank.distance = distance
    if tank.left_motor.position >= tank.distance:
        tank.distance = None
        return False
    else:
        return True

class Controller:
    def __init__(self,tank,solution,cross_detector,cL,cR):
        self.up = "u"
        self.right = "r"
        self.down = "d"
        self.left = "l"

        self.spkr = Sound()

        self.tank = tank
        self.orientation = self.up
        self.solution = solution
        self.cross_detector = cross_detector

        self.cL = cL
        self.cR = cR
        self.c_thresh = 24

    def rotate(self,turns):
        if turns == -2:
            turns = 2

        if turns == -1:
            self.tank.on(SpeedPercent(30),SpeedPercent(-30))
            while cL.reflected_light_intensity < self.c_thresh:
                pass
            self.tank.stop()
        elif turns == 1:
            self.tank.on(SpeedPercent(-30),SpeedPercent(30))
            while cR.reflected_light_intensity > self.c_thresh:
                pass
            while cR.reflected_light_intensity < self.c_thresh:
                pass
            while cR.reflected_light_intensity > self.c_thresh:
                pass

            if turns == 2:
                while cR.reflected_light_intensity < self.c_thresh:
                    pass
                while cR.reflected_light_intensity > self.c_thresh:
                    pass
            self.tank.stop()

    def change_dir(self,direction):
        l = {"u":"lurd",
                "r":"urdl",
                "l":"dlur",
                "d":"rdlu"}[self.orientation]
        i = 0
        while l[i] != direction:
            i += 1
        self.orientation= direction

        self.tank.on_for_degrees(SpeedPercent(30),SpeedPercent(30),80),

#        for u in range(i+1):
#            self.spkr.beep()
#            time.sleep(0.1)

        if i != 1:
            self.rotate(i-1)
        
        

    def run(self):
        for action in self.solution:
            self.change_dir(action.lower())

            self.tank.follow_line(
                kp=11.3, ki=0.05, kd=3.2,
                speed=SpeedPercent(30),
                follow_for=follow_until_color,
                sensor=self.cross_detector,
                color=1
                )
            if action.isupper():
            
                self.tank.on_for_degrees(SpeedPercent(30),SpeedPercent(30),30)

                self.tank.follow_line(
                        kp=11.3, ki=0.05, kd=3.2,
                        speed=SpeedPercent(30),
                        follow_for=follow_for_distance,
                        distance=470
                        )

                self.tank.on_for_degrees(SpeedPercent(-30),SpeedPercent(-30),470)




tank = MoveTank(OUTPUT_A,OUTPUT_B)
cR = ColorSensor(INPUT_1)
cL = ColorSensor(INPUT_2)
tank.cs = cR
con = Controller(tank,"ur",cL,cL,cR)

con.run()
