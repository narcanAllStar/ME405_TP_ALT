import serial


# Write a setpoint, read a position, write a setpoint...
# store each position and time
# plot the result at the end of the test
class SerialManager:
    
    def __init__(self, COMPORT, BAUDRATE):
        self.COMPORT = COMPORT
        self.BAUDRATE = BAUDRATE
        self.serial_port = serial.Serial(port = self.COMPORT, baudrate = self.BAUDRATE, stopbits = 1, timeout = 3)

    def getComport(self):
        return self.COMPORT
    
    def getBaudrate(self):
        return self.BAUDRATE
    
    # write to the serial to perform step responses with the controller
    # - writing a consistent setpoint for the controller
    def writeToVCP(self, line):
        with self.serial_port as s_port:
            s_out = line.encode()
            s_port.write(s_out)
            s_port.flush()
        s_port.close()

    # We're getting memory allocation errors. We need to do this more efficiently!
    def readFromVCP(self):
        comOutput = []
        line = ""

        with self.serial_port as s_port:
            charIn = s_port.read().decode()
            while charIn != '':
                line = line + charIn
                # print(str(s_port.in_waiting) + " bytes in waiting")
                # print("charIn: " + str(charIn))
                if charIn == '!':
                    comOutput.append(line)
                    line = ""
                charIn = s_port.read().decode()

            s_port.flush()
        s_port.close()

        return comOutput