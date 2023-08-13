import closed_loop_controller
import motor_driver, encoder, pyb, time

enable1 = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.OUT_PP)
# enable2 = pyb.Pin(pyb.Pin.cpu.C1, pyb.Pin.OUT_PP)

# Testing new enable functionality
# master_enable = pyb.Pin(pyb.Pin.cpu.A8, pyb.Pin.OUT_PP)
roller_enable = pyb.Pin(pyb.Pin.cpu.A7, pyb.Pin.OUT_PP)
trigger_enable = pyb.Pin(pyb.Pin.cpu.A9, pyb.Pin.OUT_PP)

# master_enable.low()
roller_enable.low()
trigger_enable.low()

#Testing input pins
start_button = pyb.Pin(pyb.Pin.cpu.B0, pyb.Pin.IN)
e_stop_disengaged = pyb.Pin(pyb.Pin.cpu.A4, pyb.Pin.IN) # remains high even when the button is pressed
e_stop_engaged = pyb.Pin(pyb.Pin.cpu.C0, pyb.Pin.IN)

# #defining motor inputs
# # refactored for ME 405 hardware
input1 = pyb.Pin.cpu.B4
input2 = pyb.Pin.cpu.B5
# input3 = pyb.Pin.cpu.A0
# input4 = pyb.Pin.cpu.A1
#
timer1 = pyb.Timer(3, freq = 20000)
# timer2 = pyb.Timer(5, freq = 20000)
#
# #creating motor driver / motor objects
# # enable pin, input1, input2, timer
m1_driver = motor_driver.MotorDriver(enable1, input1, input2, timer1)
m1 = m1_driver.motor(input1, input2, 1, 2, "MOTOR A")
# m2_driver = motor_driver.MotorDriver(enable2, input3, input4, timer2)
# m2 = m2_driver.motor(input3, input4, 1, 2, "MOTOR B")

degree_conversion = 66 # ticks per degree
c = closed_loop_controller.Closed_loop_controller()
c.set_kp(10)

print("Initiating encoder hardware...")
encoder_A = encoder.Encoder(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4, ID="ENCODER A")
# encoder_B = encoder.Encoder(pyb.Pin.cpu.C6, pyb.Pin.cpu.C7, 3, ID="ENCODER B")
encoder_A.zero()
print("done")

master_enable.high()

msg1 = False
msg2 = False
msg3 = False
e_stop_flag = False

print("Ready for commands")

while True:
    if not msg2:
        print("Press start button when ready to run controller")
        msg2 = True

    if (e_stop_engaged.value()==1):
        # master_enable.low()
        m1.coast()
        m1_driver.disable()
        # m2_driver.disable()
        m1.set_duty(0)
        # m2.set_duty(0)
        if not msg1:
            print("EMERGENCY STOP ENGAGED")
            msg1 = True
            e_stop_flag = True

    elif(e_stop_engaged.value() == 0 and e_stop_flag):
        e_stop_flag = False
        # m2_driver.enable()
        input("Reposition turret and press <ENTER> when ready...")
        m1.set_duty(0)
        m1_driver.enable()

        encoder_A.zero()
        time.sleep(.25)
        encoder_A.update()
        time.sleep(.25)
        msg2 = False

    if (start_button.value()==1 and e_stop_engaged.value() == 0):
        degrees = int(input("Enter a setpoint value in degrees: "))
        m1_driver.enable()
        c.set_yaw_degrees(degrees)
        position = encoder_A.read()
        encoder_A.update()

        while (position/66 != c.get_setpoint() and e_stop_engaged.value() == 0):

            duty = c.run(position)
            m1.set_duty(duty)
            encoder_A.update()
            position = encoder_A.read()

        msg2 = False

