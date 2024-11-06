# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       krizz                                                        #
# 	Created:      10/30/2024, 10:13:33 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *


#Constants
IDLE = 0
LINEFOLLOW = 2

error = 5

#65-72 on black
#50-55 White
upperBound = 27
lowerBound = 18
#Definitions

brain=Brain()

currentState = IDLE

leftLine = Line(brain.three_wire_port.a)
rightLine = Line(brain.three_wire_port.b)

controller = Controller()

leftMotor = Motor(Ports.PORT1,GearSetting.RATIO_18_1, False)
rightMotor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
armMotor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True) 

armMotor.set_stopping(HOLD)

#Main Functoin

def mainFunction():
    global currentState
    if (currentState == IDLE):
        leftMotor.stop()
        rightMotor.stop()
        if(controller.buttonA.pressing()):
            print("IDLE -> LINE FOLLOW")
            currentState = LINEFOLLOW
        if(controller.buttonX.pressing()):
            print(rightLine.reflectivity())
            print(leftLine.reflectivity())
    
    if (currentState == LINEFOLLOW):
        #if(leftLine.reflectivity() > rightLine.reflectivity() + error or leftLine.reflectivity() > rightLine.reflectivity() - error):
        if(lowerBound < leftLine.reflectivity() < upperBound and (rightLine.reflectivity() > upperBound or rightLine.reflectivity() < lowerBound)):
            leftMotor.spin(FORWARD, 150)
            rightMotor.spin(FORWARD, 100)
            if(controller.buttonB.pressing()):
                currentState = IDLE
        
        #elif(leftLine.reflectivity() < rightLine.reflectivity() + error or leftLine.reflectivity() < rightLine.reflectivity() - error):
        if(lowerBound < rightLine.reflectivity() < upperBound and (leftLine.reflectivity() > upperBound or leftLine.reflectivity() < lowerBound)):           
            leftMotor.spin(FORWARD, 100)
            rightMotor.spin(FORWARD, 150)
            if(controller.buttonB.pressing()):
                currentState = IDLE
       
        #elif(rightLine.reflectivity() + error < leftLine.reflectivity() < rightLine.reflectivity() + error):
        if(lowerBound < rightLine.reflectivity() < upperBound and lowerBound < leftLine.reflectivity() < upperBound):   
            leftMotor.spin(FORWARD, 125)
            rightMotor.spin(FORWARD, 125)
            if(controller.buttonB.pressing()):
                currentState = IDLE
    
        if((rightLine.reflectivity() > upperBound or rightLine.reflectivity() < lowerBound) and (leftLine.reflectivity() > upperBound or leftLine.reflectivity() < lowerBound)):
            print("NO LINE DETECTED")
            print("LINE FOLLOW-> IDLE")
            leftMotor.stop()
            rightMotor.stop()            
            currentState = IDLE
       
        elif(controller.buttonB.pressing()):
            print("LINE FOLLOW-> IDLE")
            leftMotor.stop()
            rightMotor.stop()
            currentState = IDLE

#loop
while True:
    print(rightLine.reflectivity())
    mainFunction()
    pass