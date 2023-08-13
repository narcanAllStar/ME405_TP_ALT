# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 21:23:02 2021

@author: jason
"""

import utime, pyb
from micropython import const

S0_init = const(0)
S1_modifyMotorTorque = const(1)
S2_modifyGainMatrix = const(2)


# devices = [motorDriver, motor_A, motor_B, controller, imu, touchPanel]
# shareList = [motor_share, delta_share, output_share, controller_share, imu_share, panel_share]
class Task_Closed_Loop_Controller:
    def __init__(self, taskID, period, devices, shares, kinVector, dbg):
        self.taskID = taskID
        
        self.kinVector = kinVector
        
        # THESE MOTOR ASSIGNMENTS ARE CORRECT!!!
        # Motor1 = the motor that causes torque about the y-axis
        self.motorAboutY = devices[2]
        # Motor2 = the motor that causes torque about the x-axis
        self.motorAboutX = devices[1]
        
        self.controller = devices[3]
        
        self.motor_share = shares[1]
        self.controller_share = shares[3]
        self.output_share = shares[2]
        
        self.period = period
        self.ser = pyb.USB_VCP()
        self.state = S0_init
        self.next_time = utime.ticks_add(utime.ticks_us(), self.period)
        
        self.systemCounter = 0
        self.posK = const(.00005)
        self.negK = const(-.00005)
        self.dbg = dbg
        
    def run(self):

        # self.controller_share.write('closedLoopMotor1')

        if (self.controller.active()):
            self.balanceSystem()
        
        action = self.controller_share.read()
        # debugging only
        
        current_time = utime.ticks_us()
        
        if (utime.ticks_diff(current_time, self.next_time) >= 0):
            if (self.state == S0_init):

                if (action == 0):
                    self.transition_to(S1_modifyMotorTorque)
                    self.controller.toggleActive()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)

                if (action == 1):
                    self.transition_to(S1_modifyMotorTorque)
                    self.balanceSystem()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                if (action == 2):
                    self.transition_to(S2_modifyGainMatrix)
                    self.controller.saveGainMatrices()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                if (action == 3):
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                
                elif (action == 11):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #decrementing k1
                    self.controller.modifyGainMatrix((self.negK,0,0,0), "Kx")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 12):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #decrementing k2
                    self.controller.modifyGainMatrix((0,self.negK,0,0), "Kx")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 13):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #decrementing k3
                    self.controller.modifyGainMatrix((0,0,self.negK,0), "Kx")
                    self.controller.displayGainMatrix()
                    
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 14):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #decrementing k4
                    self.controller.modifyGainMatrix((0,0,0,self.negK), "Kx")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 17):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #incrementing k1
                    self.controller.modifyGainMatrix((self.posK,0,0,0), "Kx")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 18):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #incrementing k2
                    self.controller.modifyGainMatrix((0,self.posK,0,0), "Kx")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 19):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #incrementing k3
                    self.controller.modifyGainMatrix((0,0,self.posK,0), "Kx")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 20):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #incrementing k4
                    self.controller.modifyGainMatrix((0,0,0,self.posK), "Kx")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 21):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #decrementing k1
                    self.controller.modifyGainMatrix((self.negK,0,0,0), "Ky")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 22):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #decrementing k2
                    self.controller.modifyGainMatrix((0,self.negK,0,0), "Ky")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 23):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #decrementing k3
                    self.controller.modifyGainMatrix((0,0,self.negK,0), "Ky")
                    self.controller.displayGainMatrix()
                    
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 24):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #decrementing k4
                    self.controller.modifyGainMatrix((0,0,0,self.negK), "Ky")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 27):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #incrementing k1
                    self.controller.modifyGainMatrix((self.posK,0,0,0), "Ky")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 28):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #incrementing k2
                    self.controller.modifyGainMatrix((0,self.posK,0,0), "Ky")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 29):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #incrementing k3
                    self.controller.modifyGainMatrix((0,0,self.posK,0), "Ky")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
                elif (action == 30):
                    self.transition_to(S2_modifyGainMatrix)
                    
                    #incrementing k4
                    self.controller.modifyGainMatrix((0,0,0,self.posK), "Ky")
                    self.controller.displayGainMatrix()
                    self.controller_share.write(None)
                    self.transition_to(S0_init)
                    
            else:
                self.transition_to(S0_init)
                
            self.next_time = utime.ticks_add(self.next_time, self.period)
            self.systemCounter += 1
    
    def balanceSystem(self):
        xVector = (self.kinVector.getX(), self.kinVector.getThetaY(),
                   self.kinVector.getXDot(), self.kinVector.getOmegaY())
        
        yVector = (self.kinVector.getY(), self.kinVector.getThetaX(),
                   self.kinVector.getYDot(), self.kinVector.getOmegaY())
        
        self.controller.computeTorques((yVector, xVector))
        
        # (xDutyCycle, yDutyCycle)
        dutyAboutX = self.controller.getDutyVector()[0]
        dutyAboutY = self.controller.getDutyVector()[1]
        
        # for debugging
        # if (self.systemCounter % 10000 == 1):
        #     print("Mx: " + str(dutyAboutX))
        #     print("My: " + str(dutyAboutY))
        #     self.systemCounter = 0
        
        self.motorAboutX.setDuty(dutyAboutX)
        self.motorAboutY.setDuty(dutyAboutY)
    
    def collectBufferedInput(self, msg):
        print('{0} '.format(msg), end = '')
        
        userInput = str(self.ser.read(2))
        if (len(userInput) > 4):
            t = userInput[2:4]
        else:
            t = userInput[2:3]
        temp = list([])
        
        # hitting the 'enter' key sends \r character to the VCP
        while (t != '\\r'):
            
            # append the information in the VCP to "duty" only if it is a digit
            if (t.isdigit()):
                # print('t is a digit')
                print ('{0}'.format(t), end = '')
                temp.append(t)
            
            userInput = str(self.ser.read(2))
            if (len(userInput) > 4):
                t = userInput[2:4]
            else:
                t = userInput[2:3]
            
            # NOTE: everytime we read values from the VCP, it then EMPTIES the VCP
            # We need to store the value of the VCP in a temp variable if we wish to use it later
        output = ''.join(map(str, temp))
        
        return output
    
    def transition_to(self, new_state):
        ''' @brief      Transitions the FSM to a new state
            @details    Optionally a debugging message can be printed
                        if the dbg flag is set when the task object is created.
            @param      new_state The state to transition to.
        '''
        if (self.dbg):
            print('{:}: S{:}->S{:}'.format(self.taskID ,self.state,new_state))
        self.state = new_state