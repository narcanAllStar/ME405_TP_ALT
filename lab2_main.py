import pyb, motor_driver, encoder, closed_loop_controller, utime
from ulab import numpy as np

def writeTo(external, test_results, test_num):
    print("Writing test results to UART...",end='')
    index = 0
    while index < len(test_results):
        x = test_results[index, 0]
        y = test_results[index, 1]
        point = (str(x) + "," + str(y) + "!").encode()
        # # vector = test_results(index)
        # print(str(x) + "," + str(y))
        if test_num ==1:
            print(point)
        external.write(point)
        index +=1

    print("done")

def readFrom(external):
    test_data = external.read().decode()
    line = test_data.split(',')
    # print("Gain: %s\t\tSetpoint: %s"%(line[0], line[1]))

    return float(line[0]), float(line[1])

def initializeUART():
    print("Initializing UART...",end='')
    BAUDRATE = 115200
    external_device = pyb.UART(2, baudrate=BAUDRATE)
    external_device.init(bits=8, baudrate=BAUDRATE, parity=None, stop=1, read_buf_len=0)
    print('done')
    return external_device

def initializeHardware():
    print("Initializing hardware...",end='')
    # enable any motor and encoder pins, probaby imported
    enable1 = pyb.Pin(pyb.Pin.cpu.A10, pyb.Pin.OUT_PP)
    input1 = pyb.Pin.cpu.B4
    input2 = pyb.Pin.cpu.B5
    timer1 = pyb.Timer(3, freq=20000)

    # Creating motor 1 objects
    motor_1_driver = motor_driver.MotorDriver(enable1, input1, input2, timer1)
    print("motor_1_driver...",end='')
    motor_1 = motor_1_driver.motor(input1, input2, 1, 2, "MOTOR A")
    print("motor_1...",end='')

    # Creating encoder object for motor 1
    encoder_A = encoder.Encoder(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4, ID="ENCODER A")
    print("encoder_A...",end='')

    # Creating controller object
    controller1 = closed_loop_controller.Closed_loop_controller()
    print("controller_1...",end='')
    print("done")
    return [encoder_A, motor_1_driver, motor_1, controller1]

def runControllerTest(gain, setpoint, enc, driver, motor, controller, testNum):
    print("Running controller test " + str(testNum) + "...",end='')
    runtime = 5500  # time in milliseconds
    step = 0.1
    size = 500

    results = np.ones((int(size), 2))

    # Starting controller tests
    controller.set_kp(gain)
    controller.set_setpoint(setpoint)

    rowIndex = 0

    enc.update()
    enc.zero()
    driver.enable()

    offset = utime.ticks_ms()
    current_time = utime.ticks_ms()
    timer_value_ms = 0

    while utime.ticks_diff(current_time, offset) < runtime and rowIndex < size:

        enc.update()
        current_position = enc.read()

        results[rowIndex, 0] = timer_value_ms
        results[rowIndex, 1] = current_position
        duty = controller.run(current_position)
        motor.set_duty(duty)

        if testNum == 1:
            print(results[rowIndex, 1])

        rowIndex +=1
        utime.sleep_ms(10)
        current_time = utime.ticks_ms()
        timer_value_ms += 10

    motor.set_duty(0)
    driver.disable()
    print("done")
    # print("# Data Points: " + str(len(results)))
    # print("Final row index: " + str(rowIndex))
    return results


if __name__ == '__main__':
    print("*** ME 405 Lab 2 ***")
    # lab 2
    print("Disabling REPL on UART 2...", end='')
    pyb.repl_uart(None)
    print("done")

    # initializing attached hardware
    hardware = initializeHardware()
    encoder = hardware[0]
    driver_m1 = hardware[1]
    m1 = hardware[2]
    controller = hardware[3]

    msgVisible = False
    testCounter = 1

    try:
        # Establishing serial communications with external PC
        external = initializeUART()

        while True:

            if (external.any() > 0):
                print("Reading data from COMPORT...",end='')
                test_params = readFrom(external)
                print("done")
                msgVisible = False

                gain = test_params[0]
                setpoint = int(test_params[1])

                # run the test loop and deal with timers in this function
                test_results = runControllerTest(gain, setpoint, encoder, driver_m1, m1, controller, testCounter)
                writeTo(external, test_results, testCounter)
                testCounter +=1
                if testCounter > 3:
                    testCounter = 1
            else:
                if not msgVisible:
                    print("Waiting for input...")
                    msgVisible = True
                pass

    except KeyboardInterrupt:
        m1.set_duty(0)
        driver_m1.disable()
        print('leaving')