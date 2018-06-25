import sys
import time
import os
from numpy import interp
from Phidget22.Devices.RCServo import *
from Phidget22.Devices.DCMotor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
import pygame

import platform

DC_MOTOR_PORT = 0
SERVO_MOTOR_PORT = 1
SERVO_MOTOR_CHANNEL = 15
HUB_SERIAL_NUM = 529516


if platform.system() == "Darwin":
    SWITCH_MODE_BTN = 10
    STOP_BTN = 12
    STEER_AXIS = 0
    THROTTLE_AXIS = 5
    GEAR_CHANGE_AXIS = 3
elif platform.system() == "Linux":
    SWITCH_MODE_BTN = 8
    STOP_BTN = 1
    STEER_AXIS = 0
    THROTTLE_AXIS = 5
    GEAR_CHANGE_AXIS = 4

try:
    servo_ch = RCServo()
    motor_ch = DCMotor()
except RuntimeError as e:
    print("Runtime Exception, ", e)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

def RCServoAttached(self):
    try:
        attached = self
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % attached.getLibraryVersion())
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("Channel Name: %s" % attached.getChannelName())
        print("Device ID: %d" % attached.getDeviceID())
        print("Device Version: %d" % attached.getDeviceVersion())
        print("Device Name: %s" % attached.getDeviceName())
        print("Device Class: %d" % attached.getDeviceClass())
        print("\n")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   
    
def RCServoDetached(self):
    detached = self
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   

def ErrorEvent(self, eCode, description):
    print("Error %i : %s" % (eCode, description))

def PositionChangeHandler(self, position):
    print("Position: %f" % position)

def DC_MotorAttached(self):
    ph = self
    ph.setDataInterval(1000)
    print("DC motor attached")

def DC_MotorDeteched(self):
    print("DC motor detatched")

def DC_MotorError(self, errorCode, errorString):
    print("DC motor error :", errorCode, errorString)

def DC_MotorVelocityUpdateHandler(self, velocity):
    print("DC motor speed: ", str(velocity))


try:

    motor_ch.setDeviceSerialNumber(HUB_SERIAL_NUM)
    motor_ch.setHubPort(DC_MOTOR_PORT)
    motor_ch.setChannel(0)

    motor_ch.setOnAttachHandler(DC_MotorAttached)
    motor_ch.setOnDetachHandler(DC_MotorDeteched)
    motor_ch.setOnErrorHandler(DC_MotorError)
    motor_ch.setOnVelocityUpdateHandler(DC_MotorVelocityUpdateHandler)



    servo_ch.setOnAttachHandler(RCServoAttached)
    servo_ch.setOnDetachHandler(RCServoDetached)
    servo_ch.setOnErrorHandler(ErrorEvent)
    servo_ch.setOnPositionChangeHandler(PositionChangeHandler)

    servo_ch.setDeviceSerialNumber(HUB_SERIAL_NUM)
    servo_ch.setHubPort(SERVO_MOTOR_PORT)
    servo_ch.setChannel(SERVO_MOTOR_CHANNEL)

    print("Waiting for the Phidget RCServo Object to be attached...")
    servo_ch.openWaitForAttachment(5000)
    motor_ch.openWaitForAttachment(5000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)


servo_ch.setMinPulseWidth(500.0)
servo_ch.setMaxPulseWidth(2500.0)

servo_ch.setTargetPosition(90)
servo_ch.setEngaged(1)

motor_ch.setCurrentLimit(5.0)

# for headless joystick reading
os.putenv('DISPLAY', ':0.0')

pygame.init()
pygame.display.set_mode((1, 1))
pyjs = pygame.joystick

js = pyjs.Joystick(0)
js.init()
should_stop = False
ai_mode = False
ai_servo_direction = 1
motor_direction = 1
ai_motor_direction = 1

while not should_stop:
    for ev in pygame.event.get(pygame.JOYBUTTONDOWN):
        print("button pressed:", ev.button)
        if ev.button == STOP_BTN:
            print("stop button pressed")
            should_stop = True
        if ev.button == SWITCH_MODE_BTN:
            print("toggleing ai mode")
            ai_mode = not ai_mode

    if ai_mode:
        new_position = servo_ch.getPosition() + 10*ai_servo_direction
        if new_position < 50 or new_position > 130:
            ai_servo_direction = ai_servo_direction * (-1)
        servo_ch.setTargetPosition(new_position)
        print("servo val from ai:", new_position)

        new_velocity = motor_ch.getVelocity() + 0.1*ai_motor_direction
        if new_velocity > 0.25 or new_velocity < -0.25:
            ai_direction = ai_motor_direction * (-1)
        v = min(max(new_velocity, -0.25), 0.25)
        print("motor v from ai: ", v)
        motor_ch.setTargetVelocity(v)

        time.sleep(2)
    else:
        for ev in pygame.event.get(pygame.JOYAXISMOTION):
            if ev.axis == STEER_AXIS:
                val = interp(ev.value, [-1, 1], [50,130])
                print("val from joy stick:", val)
                servo_ch.setTargetPosition(val)
            if ev.axis == GEAR_CHANGE_AXIS:
                if ev.value < (-0.7):
                    motor_direction = 1
                    print("dirction changed to Forward")
                elif ev.value > (0.7):
                    motor_direction = -1
                    print("dirction changed to Backward")
            if ev.axis == THROTTLE_AXIS:
                val = interp(ev.value, [-1, 1], [0,1])
                motor_ch.setTargetVelocity(val * motor_direction)

try:
    servo_ch.close()
    motor_ch.close()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1) 
print("Closed RCServo device")
exit(0)
                     
