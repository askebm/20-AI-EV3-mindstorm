#!/usr/bin/env python3
from ev3dev2.motor import *
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_4
from ev3dev2.sensor.lego import *
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.wheel import EV3Tire
import time


def follow_until_color(tank,sensor1,sensor2,c_thresh = 20):
    if sensor1.reflected_light_intensity  < c_thresh and \
            sensor2.reflected_light_intensity < c_thresh :
        return False
    else:
        return True

def follow_for_distance(tank,distance):
    if not hasattr(tank, 'distance') or tank.distance is None:
        tank.left_motor.position = 0
        tank.distance = distance
    if abs(tank.left_motor.position) >= tank.distance:
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

    def follow_line(self,interval=0.005,direction=1,condition_func = lambda tank=None : True,**kwargs):
        default_speed = direction*30
        speed_delta = direction*1

        left_speed = default_speed
        right_speed = default_speed
        while condition_func(tank=self.tank , **kwargs):
            
            right_value = self.cR.reflected_light_intensity
            left_value = self.cL.reflected_light_intensity

            
            if left_value < self.c_thresh and right_value < self.c_thresh:
                pass
            elif left_value < self.c_thresh:
                #TURN LEFT
                left_speed += speed_delta
                right_speed -= speed_delta

            elif right_value < self.c_thresh:
                #TURN RIGHT
                left_speed -= speed_delta
                right_speed += speed_delta

            else:
                left_speed = default_speed
                right_speed = default_speed

                if left_speed < default_speed:
                    left_speed += speed_delta
                elif left_speed > default_speed:
                    left_speed -= speed_delta

                if right_speed < default_speed:
                    right_speed += speed_delta
                elif right_speed > default_speed:
                    right_speed -= speed_delta
            self.tank.on(SpeedPercent(left_speed),SpeedPercent(right_speed))
            time.sleep(interval)




    def rotate(self,turns):
        turn_deg = 170

        if turns == -2:
            turns = 2

        if turns == -1:
            self.tank.turn_right(SpeedPercent(30),70)

        elif turns == 1:
            self.tank.turn_left(SpeedPercent(30),70)

        elif turns == 2:
            self.tank.turn_left(SpeedPercent(30),140)



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

        for u in range(i+1):
            self.spkr.beep()
            time.sleep(0.1)

        self.rotate(i-1)
        
        

    def run(self):
        for action in self.solution:
            self.change_dir(action.lower())

            self.follow_line(
                    condition_func = follow_until_color,
                    sensor1=self.cL,
                    sensor2=self.cR
                    )


            if action.isupper():
            
                self.spkr.tone([(392,350,100),(700,350,100)],play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
                self.tank.on_for_degrees(SpeedPercent(30),SpeedPercent(30),30)

                self.follow_line(
                        condition_func=follow_for_distance,
                        distance=470
                        )


#                tmp_cL =self.cL
#                tmp_cR =self.cR
#
#                self.cL = tmp_cR
#                self.cR = tmp_cL

                self.follow_line(
                        direction=-1,
                        condition_func=follow_for_distance,
                        distance=470
                        )

#                self.cL = tmp_cL
#                self.cR = tmp_cR

                        

        self.tank.stop()


tank = MoveDifferential(OUTPUT_A,OUTPUT_B,EV3Tire,120)
cR = ColorSensor(INPUT_1)
cL = ColorSensor(INPUT_2)
tank.cs = cR
con = Controller(tank,"lllldlluRRUdRRRdrUUruulldRRdldlluLuulldRurDDullDRdRRRdrUUruurrdLulDulldRddlllldlluRRRRRdrUUdlllluurDldRRRdrU",cL,cL,cR)



con.run()


