#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  stepper_driver.py
#  Travis Barrett
#  Copyright 2019  
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from time import sleep
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

DELAY = 0.001 #delay between step commands
DIRx = 24 #gpio pin for direction x
STEPx = 23 #gpio pin for step x
DIRy = 8 #gpio pin for direction y
STEPy = 25 #gpio pin for step y
CW = 1 #clockwise direction
CCW = 0 #counter clockwise direction
SPR = 200 #steps per rotation on full step
MODE = (14,15,18)
MS = 32

azimuth = 0 #memory of x axis in steps
altitude = (-180 * MS)    #memory of y axis in steps

MICROSTEPS = {1: (0, 0, 0),
	      2: (1, 0, 0),
	      4: (0, 1, 0),
	      8: (1, 1, 0),
	      16: (0, 0, 1),
	      32: (1, 0, 1),
	      128: (0, 1, 1),
	      256: (1, 1, 1)
	      }

def init():
    
    DELAY = 0.001 #delay between step commands
    DIRx = 24 #gpio pin for direction x
    STEPx = 23 #gpio pin for step x
    DIRy = 8 #gpio pin for direction y
    STEPy = 25 #gpio pin for step y
    CW = 1 #clockwise direction
    CCW = 0 #counter clockwise direction
    SPR = 200 #steps per rotation on full step
    MODE = (14,15,18)
    MS = 32
    
    azimuth = 0 #memory of x axis in steps
    altitude = (-180 * MS)    #memory of y axis in steps
    
    MICROSTEPS = {1: (0, 0, 0),
		  2: (1, 0, 0),
		  4: (0, 1, 0),
		  8: (1, 1, 0),
		  16: (0, 0, 1),
		  32: (1, 0, 1),
		  128: (0, 1, 1),
		  256: (1, 1, 1)
		  }
	
	
    
    GPIO.setup(DIRx, GPIO.OUT)
    GPIO.setup(STEPx, GPIO.OUT)
    GPIO.setup(DIRy, GPIO.OUT)
    GPIO.setup(STEPy, GPIO.OUT)
    print('Initialized')
    
    
for x in range(3): #sets mode pins
	GPIO.setup(MODE[x], GPIO.OUT)
	GPIO.output(MODE[x],MICROSTEPS[MS][x])

def DegToSteps(deg): #spr = steps per rotation, microstep = number of microsteps, deg = degrees
    ratio = (SPR * MS)/float(360)
    #print(ratio)
    steps = ratio * deg
    #print(steps)
    return int(steps)

def step(stepPin , steps): 
	
	for i in range(steps):
		GPIO.output(stepPin, GPIO.HIGH)
		sleep(DELAY)
		GPIO.output(stepPin, GPIO.LOW)
		sleep(DELAY)
		

def moveAz(desiredPos): #desiredPos should be value of steps (int) required from 0 point
	moveStepsx = int(desiredPos - azimuth)
	if moveSteps >= 0:
		GPIO.output(DIRx, CW)
		step(STEPx, moveStepsx)
		print("Done moving Azimuth")
		azimuth = desiredPos
		
	else:
		GPIO.output(DIRx, CCW)
		step(STEPx, (-1 * moveStepsx))
		print("Done moving Azimuth")
		azimuth = desiredPos


def moveAlt(desiredPos): #desiredPos should be value of steps (int) required from 0 point
	moveStepsy = int(desiredPos - altitude)
	if moveSteps >= 0:
		GPIO.output(DIRy, CW)
		step(STEPy, moveStepsy)
		print("Done moving Altitude")
		altitude = desiredPos
		
	else:
		GPIO.output(DIRy, CCW)
		step(STEPy, (-1 * moveStepsy))
		print("Done moving Altitude")
		altitude = desiredPos

def shutdownSteppers():
	Print("Shutting Down")
	moveAz(0)
	moveElev((-180*MS))
	GPIO.cleanup()
	Print("Done")
	
	
# def main(args):
    # # azimuth = 0
    # # elevation = -180
    
    
    # # DIRx = 24 #gpio pin for direction x
    # # STEPx = 23 #gpio pin for step x
    # # DIRy = 8 #gpio pin for direction y
    # # STEPy = 25 #gpio pin for step y
    # # CW = 1 #clockwise direction
    # # CCW = 0 #counter clockwise direction
    # # SPR = 200 #steps per rotation on full step
    # # MODE = (14,15,18)
    # # MS = 32
    
    # # MICROSTEPS = {1: (0, 0, 0),
              # # 2: (1, 0, 0),
              # # 4: (0, 1, 0),
              # # 8: (1, 1, 0),
              # # 16: (0, 0, 1),
              # # 32: (1, 0, 1),
              # # 128: (0, 1, 1),
              # # 256: (1, 1, 1)
              # # }
    
    
    # # GPIO.setmode(GPIO.BCM)
    # # GPIO.setup(DIRx, GPIO.OUT)
    # # GPIO.setup(STEPx, GPIO.OUT)
    # # GPIO.setup(DIRy, GPIO.OUT)
    # # GPIO.setup(STEPy, GPIO.OUT)
    
    # # for x in range(3): #sets mode pins
        # # GPIO.setup(MODE[x], GPIO.OUT)
        # # GPIO.output(MODE[x],MICROSTEPS[MS][x])
        
    
    # try:
        # while True:
            # GPIO.output(DIRx, int(input("Enter direction x: 1 or 0 \n")))  # Set direction x
            # GPIO.output(DIRy, int(input("Enter direction y: 1 or 0 \n")))  # Set direction y
            # degx = input("enter degrees x\n")
            # degy = input("enter degrees y\n")
            
            # stepsx = DegToSteps(degx)
            # stepsy = DegToSteps(degy)
            
            # for x in range(stepsx):
                # GPIO.output(STEPx, GPIO.HIGH)
                # sleep(0.0001)
                # GPIO.output(STEPx, GPIO.LOW)
                # #print(x)
                # sleep(0.0001)
            
            # for y in range(stepsy):
                # GPIO.output(STEPy, GPIO.HIGH)
                # sleep(0.0001)
                # GPIO.output(STEPy, GPIO.LOW)
                # #print(y)
                # sleep(0.0001)
            
            
        
        

    # except KeyboardInterrupt:
        # print ("\nCtrl-C pressed.  Stopping GPIO and exiting...")
    # finally:
        
        # GPIO.cleanup()
    
    
    
    # return 0

# if __name__ == '__main__':
    # import sys
    # sys.exit(main(sys.argv))
